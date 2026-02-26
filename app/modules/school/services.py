from sqlalchemy.orm import Session 
from sqlalchemy import or_
from fastapi import HTTPException, status 
# from app.core.base_repo import BaseRepository
from .repository import UniversityRepository
from .models import (
    University,
    Program,
    Department,
    Faculty,
    Course,
    Module,
)
from .schemas import (
    FacultyCreateRequest,
    UniversityCreateRequest,
    UniversityUpdateRequest,
)
from ..address.schemas import AddressCreateRequest
from ..address.services import AddressService
from ..address.repository import AddressRepository
from app.core.logger import logger


class UniversityService:
    def __init__(self, db:Session):
        # self.repo = BaseRepository(University, db)
        self.repo = UniversityRepository(db)
        self.db = db

    def get_university(self, university_id: str) -> University:
        university = self.repo.get(university_id)
        if not university:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="University not found"
            )
        return university 

    
    def create_university(self, uni_data: UniversityCreateRequest, address_data: AddressCreateRequest) -> University:
        # Business Logic: Check if name already exists
        # 1. Business Logic: Check duplicates
        existing = self.db.query(University).filter(
            or_(
                University.name == uni_data.name, 
                University.code == uni_data.code
            )
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="University with this name/code already exists"
            )
        
        try:
            # 2. Create the Model instance
            new_university = University(
                name=uni_data.name,
                code=uni_data.code
            )

            # 3. Handle Address Logic
            if address_data:
                # We reuse the logic from your address creator
                # Note: In a true UoW, create_address should not commit internally
                address_service = AddressService(
                    AddressRepository(self.db),
                )
                address = address_service.create_address(address_data)
                # address_id = address_service.create_address(address_data)
                new_university.address_id = str(address.address_id)

            # 4. Atomic Save
            self.db.add(new_university)
            self.db.commit()
            self.db.refresh(new_university)
            return new_university

        except Exception as e:
            self.db.rollback()
            # Log the actual error here for developers
            print(f"Error creating university: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Failed to create university record"
            )
  
    def update_university(self, uni_id: str, data: UniversityUpdateRequest) -> University:
        existing = self.get_university(uni_id)
        
        updated_university = self.repo.update(existing, data)
        self.db.commit()
        self.db.refresh(updated_university)
        return updated_university
        
   
    def get_universities(self):
        universities = self.repo.get_multi(skip=0, limit=100)
        return universities
    
    def get_by_name_or_code(self, code:str=None, name:str=None):

        if code is None and name is None:
            raise ValueError("Either Code or Name should be provided")
        if code:
            uni = self.repo.get_by_code(code)
        
        if name:
            uni = self.repo.get_by_name(name)

        logger.info("[Address ]", uni.address)
        return uni
        


class FacultyService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_faculty(self, id: str) -> Faculty:
        return self.db.get(Faculty, id)

    def create_faculty(self, faculty_data: FacultyCreateRequest) -> Faculty:
        existing = self.db.query(Faculty).filter(
            or_(
                Faculty.name==faculty_data.name,
                Faculty.code==faculty_data.code,
            )
            ).first()
        
        
        if  existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Faculty already registered"
            )
        
        university = self.db.query(University).filter(University.code==faculty_data.university_code).first()

        if not university:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"University with code '{faculty_data.university_code}' Not found!",
                )
        
        try:
            faculty = Faculty(
                name=faculty_data.name,
                code=faculty_data.code,
                university_id = university.id
            )
            self.db.add(faculty)
            self.db.commit()
            self.db.refresh(faculty)
                
            return faculty
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{str(e)}"
                )
        
