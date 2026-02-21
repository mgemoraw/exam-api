from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete, insert


from app.infrastructure.database import get_db
from app.schemas.question import QuestionUploadRequest, QuestionResponse, MCQCreateRequest, ContentBlock, ContentType, OptionCreateSchema, OptionResponseSchema
from app.models.exam import Question, Option
from app.models.school import Department, Course, Module
import json
from uuid import uuid4


question_router = APIRouter(prefix="/questions", tags=["questions"])


@question_router.get("/{question_id}", response_model=QuestionResponse)
async def get_question(question_id: str, db: AsyncSession = Depends(get_db)):
    question = await db.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    options = await db.execute(select(Option).where(Option.question_id == question_id))
    options = options.scalars().all()
    
    return QuestionResponse(
        id=question.id,
        department=question.department,
        course=question.course,
        module=question.module,
        question=[ContentBlock(type=ContentType.TEXT, content=question.question)],
        options={option.label: OptionResponseSchema(content=json.loads(option.content)) for option in options}
    )


@question_router.post("/", response_model=QuestionResponse)
async def create_question(
    request: MCQCreateRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        # Validate Department
        result = await db.execute(
            select(Department).where(Department.name == request.department)
        )
        department = result.scalar_one_or_none()
        if not department:
            raise HTTPException(status_code=400, detail="Department not found")


        # Validate Module belongs to Department
        result = await db.execute(
            select(Module).where(
                Module.title == request.module,
                Module.department_id == department.id
            )
        )
        module = result.scalar_one_or_none()
        if not module:
            raise HTTPException(status_code=400, detail="Module not found in department")
        
        # Validate Course belongs to Department and module
        result = await db.execute(
            select(Course).where(
                Course.name == request.course,
                Course.department_id == department.id,
                Course.module_id == module.id
            )
        )
        course = result.scalar_one_or_none()
        if not course:
            raise HTTPException(status_code=400, detail="Course not found in department")
        
        # Determine correct option centrally
        correct_option = next(
            label for label, opt in request.options.items()
            if opt.is_answer
        )

        question = Question(
            id=uuid4(),
            department_id=department.id,
            course_id=course.id,
            module_id=module.id,
            content=[block.model_dump() for block in request.question],
            correct_option=correct_option
        )

        db.add(question)
        await db.flush()  # get question.id without commit

        for label, option_data in request.options.items():
            option = Option(
                id=uuid4(),
                question_id=question.id,
                label=label,
                content=[block.model_dump() for block in option_data.content]
            )
            db.add(option)

        await db.commit()
        await db.refresh(question)

        return question

    except Exception:
        await db.rollback()
        raise


@question_router.post("/upload")
async def upload_questions(
    file: UploadFile,
    db: Session = Depends(get_db)
):
    # Validate file type
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Only JSON files allowed")

    try:
        content = await file.read()
        data = json.loads(content.decode("utf-8"))

        # Validate JSON structure
        validated_data = QuestionUploadRequest(**data)

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    created_ids = []

    try:
        for item in validated_data.questions:
            question = Question(
                id=uuid4(),
                content=item.content,
                question_type=item.question_type,
                marks=item.marks,
                options=[opt.model_dump() for opt in item.options],
                correct_option=item.correct_option,
            )

            db.add(question)
            created_ids.append(question.id)

        db.commit()

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to save questions")

    return {
        "message": "Questions uploaded successfully",
        "count": len(created_ids),
        "question_ids": created_ids
    }
