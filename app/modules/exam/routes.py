from fastapi import APIRouter, Depends, HTTPException, Request


router = APIRouter(
    prefix="/exams",
    tags=['Exams'],
)


@router.get("/")
def check_exams(request: Request):
    return {
        "message": "Healthy"
    }

