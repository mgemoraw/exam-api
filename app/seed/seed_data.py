import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

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
import json 
import os 


def load_academic_structure(path:str):
    with open(path, 'r') as json_file:
        data = json_file.read()
        return json.loads(data)
 
def seed_academic_structure():
    # path to json file
    json_path = os.path.join(os.path.dirname(__file__), "academic_structure.json")

    with open(json_path, "r") as file:
        structure = json.load(file)



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
