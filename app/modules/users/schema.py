from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    


