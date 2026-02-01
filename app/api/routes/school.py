from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_
from app.core.database import get_db
from app.models.address import Address
from app.models.school import (
    Module,
    University,
    Department,
    Faculty,
    Course,
    StudentCourse,
)
from app.schemas.school import CourseCreateRequest, DepartmentCreateRequest, DepartmentResponse, FacultyCreateRequest, FacultyResponse, ModuleCreateRequest, ModuleResponse, UniversityCreateRequest, UniversityResponse
from app.schemas.address import AddressCreateRequest 
from app.utils.address import create_address
import uuid


school_router = APIRouter(
    prefix="/school",
    tags=["School"]
)


@school_router.get("/universities", response_model=list[UniversityResponse])
async def get_universities(db: Session = Depends(get_db)):

    universities = db.query(University).options(
        joinedload(University.address)
    ).all()

   
    return universities

@school_router.post("/universities")
async def create_university(university: UniversityCreateRequest, address: AddressCreateRequest=None, db: Session = Depends(get_db)):
    try:
        existing_university = db.query(University).filter(
            or_(University.name == university.name, University.code == university.code)).first()
       
        
        if existing_university:
            raise HTTPException(status_code=400, detail="University with this name/code already exists")
        
        new_university = University(
            name=university.name, 
            code=university.code,
        )

        if address is not None:
            # Here we create the address and get its ID
            # university_address = AddressCreateRequest(**address.model_dump())
            address_id = create_address(address, db)
            new_university.address_id = str(address_id)
        db.add(new_university)
        db.commit()
        db.refresh(new_university)
        return new_university
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query failed {e}") from e
    
@school_router.delete("/universities/{university_id}")
async def delete_university(university_id: uuid.UUID, db: Session = Depends(get_db)):
    university = db.query(University).filter(University.id == str(university_id)).first()
    if not university:
        raise HTTPException(status_code=404, detail="University not found")
    db.delete(university)
    db.commit()
    return {"detail": "University deleted successfully"}

    
@school_router.get("/faculties", response_model=list[FacultyResponse])
async def get_faculties(db: Session = Depends(get_db)):
    faculties = db.query(Faculty).all()
    return faculties

@school_router.post("/faculties")
async def create_faculty(data: FacultyCreateRequest, db: Session = Depends(get_db)):
    university = db.query(University).filter(University.code == data.university_code).first()
    if not university:
        raise HTTPException(status_code=404, detail="University not found for the given code")
    faculty = Faculty(
        name=data.name,
        code=data.code,
        university_id=university.id
    )

    db.add(faculty)
    db.commit()
    db.refresh(faculty)
    return faculty



@school_router.get("/departments", response_model=list[DepartmentResponse])
async def get_departments(db: Session = Depends(get_db)):
    departments = db.query(Department).all()
    return departments


@school_router.post("/departments", response_model=DepartmentResponse)
async def create_department(department: DepartmentCreateRequest, db: Session = Depends(get_db)):
    existing_department = db.query(Department).filter(
        Department.name == department.name
    ).first()

    if existing_department:
        raise HTTPException(status_code=400, detail="Department with this name already exists")
    
    university = db.query(University).filter(
        University.code == department.university_code).first()
    
    if not university:
        raise HTTPException(status_code=404, detail="University not found for the given code")
    
    faculty = db.query(Faculty).filter(
        and_(Faculty.code == department.faculty_code, Faculty.university_id == university.id)).first()
    
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found for the given code")
    
    department = Department(
        name=department.name,
        faculty_id=faculty.id
    )

    db.add(department)
    db.commit()
    db.refresh(department)
    return department


@school_router.get("/modules", response_model=list[ModuleResponse])
async def get_modules(db: Session = Depends(get_db)):
    modules = db.query(Module).all()
    return modules

@school_router.post("/modules")
async def create_module(module: ModuleCreateRequest, db: Session = Depends(get_db)):
    university = db.query(University).filter(
        University.code == module.university_code).first()
    
    if not university:
        raise HTTPException(status_code=404, detail="University not found for the given code")
    
    faculty = db.query(Faculty).filter(
        and_(Faculty.code == module.faculty_code, Faculty.university_id == university.id)).first()
    
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found for the given code")
    
    department = db.query(Department).filter(
        and_(Department.name == module.department_name, Department.faculty_id == faculty.id)).first()
    
    if not department:
        raise HTTPException(status_code=404, detail="Department not found for the given name")
    
    new_module = Module(
        title=module.title,
        description=module.description,
        faculty_id=faculty.id,
        department_id=department.id
    )

    db.add(new_module)
    db.commit()
    db.refresh(new_module)
    return new_module




@school_router.get("/courses")
async def get_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    return courses

@school_router.post("/courses")
async def create_course(course: CourseCreateRequest, db: Session = Depends(get_db)):
    existing_course = db.query(Course).filter(
        Course.code == course.code
    ).first()

    if existing_course:
        raise HTTPException(status_code=400, detail="Course with this code already exists")
    
    # search for faculty and module based on provided codes/names
    # faculty = db.query(Faculty).filter(
    #     Faculty.code == course.faculty_code
    # ).first()
    # if not faculty:
    #     raise HTTPException(status_code=404, detail="Faculty not found for the given code")

    module = db.query(Module).filter(
        Module.title == course.module_title
    ).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found for the given name")

    department = db.query(Department).filter(
        Department.name == course.department_name
    ).first()

    if not department:
        raise HTTPException(status_code=404, detail="Department not found for the given name")
    
    new_course = Course(    
    name=course.name,
    code=course.code,
    credits=course.credits,
    module_id=module.id,
    department_id=department.id
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course


@school_router.delete("/courses/{course_id}")
async def delete_course(course_id: uuid.UUID, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == str(course_id)).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    db.commit()
    return {"detail": "Course deleted successfully"}


@school_router.get("/student-courses/{student_id}")
async def get_student_courses(student_id: int, db: Session = Depends(get_db)):
    student_courses = db.query(StudentCourse).filter(StudentCourse.student_id == student_id).all()
    return student_courses


@school_router.get("/student-course/{student_course_id}")
async def get_student_course(student_course_id: int, db: Session = Depends(get_db)):
    student_course = db.query(StudentCourse).filter(StudentCourse.id == student_course_id).first()
    if not student_course:
        raise HTTPException(status_code=404, detail="Student course not found")
    return student_course

@school_router.get("/student-courses/count/{student_id}")
async def count_student_courses(student_id: int, db: Session = Depends(get_db)):
    count = db.query(StudentCourse).filter(StudentCourse.student_id == student_id).count()
    return {"student_id": student_id, "course_count": count}


