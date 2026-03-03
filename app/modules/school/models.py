from typing import List

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, func, TEXT
from sqlalchemy.orm import relationship, Mapped,mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy
import uuid
from app.infrastructure.base import Base, MainModel
# from ..address.models import Address
# from ..question.models import Question 
# from ..user.models import Student

class University(Base):
    __tablename__ = "universities"

    # id :Mapped[str.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    id :Mapped[str] = mapped_column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    code = Column(String(100), unique=True, nullable=False)
    address_id = Column(String(36), ForeignKey("addresses.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship with Address
    address = relationship("Address", back_populates="university")
    # Relationship with Faculty
    faculties = relationship("Faculty", back_populates="university")
    schools = relationship('School', back_populates='university')
    institutes = relationship('Institute', back_populates='university')

class Institute(MainModel, Base):
    __tablename__ = "institutes"

    slug_source_field = "name"

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    university_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("universities.id"),
        nullable=False
    )
    
    university = relationship("University", back_populates="institutes")
    faculties = relationship("Faculty", back_populates="institute")
    schools = relationship("School", back_populates="institute")

    __table_args__ = (
        UniqueConstraint("slug", "university_id", name="uq_institute_slug_per_university"),
    )

    def __repr__(self):
        return f"<Institute id={self.id} slug={self.slug}>"
    

class Faculty(Base):
    __tablename__ = "faculties"

    id :Mapped[str] = mapped_column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    code = Column(String(100), unique=True, nullable=False)
    university_id = Column(String(36), ForeignKey("universities.id"), nullable=False)
    institute_id = Column(String(36), ForeignKey("institutes.id", name="fk_faculties_institute_id_institutes"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship with University
    university = relationship("University", back_populates="faculties")

    # Relationship with Department
    departments = relationship("Department", back_populates="faculty")
    programs = relationship("Program", back_populates="faculty")
    
    # # Relationship with Institute
    institute = relationship("Institute", back_populates="faculties", foreign_keys=[institute_id])


class School(MainModel, Base):
    __tablename__ = "schools"

    slug_source_field = "name"

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    university_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("universities.id"),
        nullable=False
    )
    institute_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("institutes.id"),
        nullable=False
    )
    university = relationship("University", back_populates="schools")
    institute = relationship("Institute", back_populates="schools")
    programs = relationship("Program", back_populates="school")

    __table_args__ = (
        UniqueConstraint("slug", "university_id", name="uq_school_slug_per_university"),
    )

    def __repr__(self):
        return f"<School id={self.id} slug={self.slug}>"
   


class Department(Base):
    __tablename__ = "departments"

    id :Mapped[str] = mapped_column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    years_of_study = Column(Integer, nullable=False)
    faculty_id = Column(String(36), ForeignKey("faculties.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship with Faculty
    faculty = relationship("Faculty", back_populates="departments")
    # Relationship with Module
    modules = relationship("Module", back_populates="department")
    courses = relationship("Course", back_populates="department")
    questions = relationship("Question", back_populates="department")


class Program(Base):
    __tablename__ = 'programs'
    id :Mapped[str] = mapped_column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    years_of_study = Column(Integer, nullable=False)
    level_of_study = Column(String(255), default="Bachelor of Science")
    description = Column(TEXT)
    faculty_id = Column(String(36), ForeignKey("faculties.id"), nullable=False)
    school_id = Column(String(36), ForeignKey("schools.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    faculty = relationship("Faculty", back_populates="programs")
    # modules = relationship("Module", back_populates="programs")
    courses = relationship("Course", back_populates="program")
    questions = relationship("Question", back_populates="program", foreign_keys='Question.program_id')

    students: Mapped[List['Student']] = relationship('Student', back_populates='program', cascade='delete, delete-orphan')
    exams: Mapped[List['Exam']] = relationship('Exam', back_populates='program')
    school: Mapped['School'] = relationship('School', back_populates='programs')
    

class Module(Base):
    __tablename__ = "modules"

    id :Mapped[str] = mapped_column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    department_id = Column(String(36), ForeignKey("departments.id"), nullable=False)
    # program_id = Column(String(36), ForeignKey("programs.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(TEXT, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship with Department
    department = relationship("Department", back_populates="modules")
    # program = relationship("Program", back_populates="modules")
    # Relationship with Course
    courses = relationship("Course", back_populates="module")

    questions = relationship("Question", back_populates="module")

class Course(Base):
    __tablename__ = "courses"

    id :Mapped[str] = mapped_column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    code = Column(String(100), unique=True, nullable=False)
    credits = Column(Integer, nullable=False)
    
    module_id = Column(String(36), ForeignKey("modules.id"), nullable=False)
    department_id = Column(String(36), ForeignKey("departments.id"), nullable=False)
    program_id = Column(String(36), ForeignKey("programs.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship with Department
    department = relationship("Department", back_populates="courses")
    program = relationship("Program", back_populates="courses")

    # Relationship with Module
    module = relationship("Module", back_populates="courses")
    # Relationship with StudentCourse

    student_courses = relationship("StudentCourse", back_populates="course", cascade="all, delete-orphan")

    # Relationship with Student through StudentCourse
    questions = relationship("Question", back_populates="course")
    chapters = relationship("Chapter", back_populates="course", cascade="all, delete")

    # 2. The Proxy: This allows you to do `course.students` 
    # It fetches the 'student' attribute from every 'StudentCourse' object.
    students: AssociationProxy[List["Student"]] = association_proxy(
        "student_courses", "student", 
        creator=lambda s: StudentCourse(student=s)
    )


class StudentCourse(Base):
    __tablename__ = "student_courses"

    id :Mapped[str] = mapped_column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False)
    course_id = Column(String(36), ForeignKey("courses.id"), nullable=False)
    enrollment_date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())  

    # Relationship with Student
    student = relationship("Student", back_populates="student_courses")

    # Relationship with Course
    course = relationship("Course", back_populates="student_courses")
    