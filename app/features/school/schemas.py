from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from typing import Optional, List, Dict, Union
from datetime import datetime
from enum import Enum
from app.models.exam import ExamTypeEnum
from app.schemas.address import AddressResponse

class UniversityCreateRequest(BaseModel):
    name: str
    code: str

    model_config=ConfigDict(from_attributes=True)

class UniversityResponse(BaseModel):
    id: UUID | str
    name: str
    code: str
    address_id: Optional[Union[UUID, str]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    address: Optional['AddressResponse'] = None
    model_config=ConfigDict(from_attributes=True)


class UniversityUpdateRequest(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    address_id: Optional[Union[UUID, str]] = None

    model_config=ConfigDict(from_attributes=True)


class FacultyCreateRequest(BaseModel):
    name: str
    code: str
    university_code: Optional[str]=None

    model_config=ConfigDict(from_attributes=True)


class FacultyResponse(BaseModel):
    id: UUID | str
    name: str
    code: str
    university: Optional['UniversityResponse'] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config=ConfigDict(from_attributes=True)


class DepartmentCreateRequest(BaseModel):
    name: str
    university_code: Optional[str]=None
    faculty_code: Optional[str]=None
    
    
    model_config=ConfigDict(from_attributes=True)


class DepartmentResponse(BaseModel):
    id: UUID | str
    name: str
    facuulty: Optional['FacultyResponse'] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config=ConfigDict(from_attributes=True)


class DepartmentUpdateRequest(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None

    
    model_config=ConfigDict(from_attributes=True)


class ModuleCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    university_code: Optional[str]=None
    faculty_code: Optional[str]=None
    department_name: Optional[str]=None

    model_config=ConfigDict(from_attributes=True)

class ModuleResponse(BaseModel):
    id: UUID | str
    title: str
    description: Optional[str] = None
    faculty: Optional['FacultyResponse'] = None
    department: Optional['DepartmentResponse'] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config=ConfigDict(from_attributes=True)

class ModuleUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    model_config=ConfigDict(from_attributes=True)

class CourseCreateRequest(BaseModel):
    name: str
    code: str
    credits: int
    department_name: Optional[str]=None
    module_title: Optional[str]=None

    model_config=ConfigDict(from_attributes=True)

class CourseResponse(BaseModel):
    id: UUID | str
    name: str
    code: str
    module: Optional['ModuleResponse'] = None
    department: Optional['DepartmentResponse'] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config=ConfigDict(from_attributes=True)

class CourseUpdateRequest(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None

    model_config=ConfigDict(from_attributes=True)


class ProgramCreateRequest(BaseModel):
    name: str
    university_code: str
    faculty_code: str
    year_of_study: int

    


class ProgramResponse(BaseModel):
    id: Optional[UUID] = None
    name: str
    years_of_study: int
    faculty: Optional['FacultyResponse'] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

