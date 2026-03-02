import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
# from sqlalchemy.orm import and_, or_, func
from app.db.session import async_session, SessionLocal  # your async session
from app.modules.school.models import (
    University,
    Institute,
    Program,
    Faculty,
    School,
    Department,
    Course,
    Module,
)
from app.modules.address.models import Address
from app.modules.exam.models import Exam
from app.modules.question.models import Question
from app.modules.user.models import User, Student
from app.modules.auth.models import RefreshToken
from app.modules.news.models import News

import json 
import os 
from datetime import timezone, datetime



def load_academic_structure(path:str):
    with open(path, 'r') as json_file:
        data = json_file.read()
        return json.loads(data)
 
def seed_academic_structure():
    # path to json file
    json_path = os.path.join(os.path.dirname(__file__), "academic_structure.json")
    session = SessionLocal()\
    
    with open(json_path, "r") as file:
        structure = json.load(file)

        uni_data = structure.get("university")
        uni_address = uni_data.get("address")
        address = session.execute(
            select(Address).where(
                and_(
                    Address.city==uni_address['city'],
                    Address.city==uni_address['country'],
                    Address.city==uni_address['street'],
                    Address.city==uni_address['zipcode'],
                )
            )
        )
        # Prevent duplicate seeding
        result =  session.execute(
            select(University).where(
                University.code == uni_data["code"]
            )
        )
        
        university = result.scalars().first()
        if not university:
            print("Seed data already exists.")
            # return

            university = University(
                name=uni_data["name"],
                code=uni_data['code'],
                address_id=address.id,
                )
            session.add(university)
            session.flush()

        institutes = uni_data.get("institutes")
        for ins_data in institutes:
            result =  session.execute(
                    select(Institute).where(
                        Institute.name == ins_data["name"]
                    )
                )
            institute = result.scalars().first()

            if  not institute:
                
                institute = Institute(
                    name=ins_data['name'],
                    slug_source_field="name",
                    university_id=university.id,
                    updated_at = datetime.now(timezone.utc)
                )
                session.add(institute)
                session.flush()
            
            faculties = ins_data.get("faculties")
            for fa_data in faculties:
                # Prevent duplicate seeding
                result =  session.execute(
                    select(Faculty).where(
                        Faculty.code == fa_data["code"]
                    )
                )
                faculty = result.scalars().first()
                if not faculty:
                    
                    faculty = Faculty(
                        name=fa_data['name'],
                        code=fa_data['code'],
                        university_id=university.id,
                        institute_id=institute.id,
                    )
                    session.add(faculty)
                    session.flush()

                programs = fa_data.get("programs")
                for pr_data in programs:
                     # Prevent duplicate seeding
                    result =  session.execute(
                        select(Program).where(
                            Program.name == pr_data["name"]
                        )
                    )
                    program = result.scalars().first()
                    if not program:
                        print("adding program...")
                        program = Program(
                            name=pr_data['name'],
                            # slug=pr_data['slug'],
                            years_of_study=pr_data['years_of_study'],
                            level_of_study=pr_data['level_of_study'],
                            faculty_id=faculty.id,
                            school_id = faculty.id,
                        )
                        session.add(program)
                        session.flush()

        # Finally commit changes
        session.commit()

seed_data= {}


async def seed():
    async with async_session() as session:  # type: AsyncSession
        async with session.begin():

            # Prevent duplicate seeding
            result = await session.execute(
                select(University).where(
                    University.name == seed_data["name"]
                )
            )
            existing = result.scalars().first()
            if existing:
                print("Seed data already exists.")
                return

            university = University(name=seed_data["name"])
            session.add(university)
            await session.flush()

            for inst_data in seed_data["institutes"]:
                institute = Institute(
                    name=inst_data["name"],
                    university_id=university.id,
                )
                session.add(institute)
                await session.flush()

                # Faculties
                for fac_data in inst_data.get("faculties", []):
                    faculty = Faculty(
                        name=fac_data["name"],
                        slug=fac_data["slug"],
                        institute_id=institute.id,
                    )
                    session.add(faculty)
                    await session.flush()

                    for prog_data in fac_data.get("programs", []):
                        program = Program(
                            name=prog_data["name"],
                            slug=prog_data["slug"],
                            years_of_study=prog_data["years_of_study"],
                            level_of_study=prog_data["level_of_study"],
                            faculty_id=faculty.id,
                        )
                        session.add(program)

                # Schools
                for sch_data in inst_data.get("schools", []):
                    school = School(
                        name=sch_data["name"],
                        slug=sch_data["slug"],
                        institute_id=institute.id,
                    )
                    session.add(school)
                    await session.flush()

                    for prog_data in sch_data.get("programs", []):
                        program = Program(
                            name=prog_data["name"],
                            slug=prog_data["slug"],
                            years_of_study=prog_data["years_of_study"],
                            level_of_study=prog_data["level_of_study"],
                            school_id=school.id,
                        )
                        session.add(program)
                        

        await session.commit()

    print("✅ Seeding completed successfully!")


if __name__ == "__main__":
    # asyncio.run(seed())
    seed_academic_structure()
