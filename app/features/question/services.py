
from sqlalchemy.orm import Session
from .repository import QuestionRepository
from .models import Question, Option
from ..exam.models import Exam
from .exception import QuestionExistsError
from .schemas import MCQCreateRequest
from ..school.models import Course, Faculty, Module, Program
from ..school.exception import CourseNotFoundError, ModuleNotFoundError, ProgramNotFoundError
from ..exam.exception import ExamNotFoundError

class QuestionService:
    def __init__(self, db: Session):
        self.repo = QuestionRepository(db)

        self.db = db

    def get_question(self, id:str):
        return self.repo.get(id)
    

    def create_question(self, question: MCQCreateRequest) -> Question:
        existing = self.db.query(Question).filter(Question.content==question.content).first()
        if existing:
            raise QuestionExistsError
        
        course = self.db.query(Course).filter(Course.id==question.course_id).first()

        if not course:
            raise CourseNotFoundError
        
        program = self.db.query(Program).filter(Program.id==question.program_id).first()

        if not program:
            raise CourseNotFoundError
        exam = self.db.query(Exam).filter(Exam.id==question.exam_id).first()
        
        if not exam:
            raise ExamNotFoundError

        mcq = Question(
            exam_id=exam.id,
            program_id=program.id,
            course_id=course.id,
            content=question.content,
            # options = question.options,
            answer = question.answer,
            marks=question.marks,
        )

