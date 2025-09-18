from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: str
    is_admin: bool


class UserCreate(UserBase):
    username: str
    email: str
    is_admin: bool
    password: str


class UserUpdate(UserBase):
    username: Optional[str] = None
    email: Optional[str] = None
    is_admin: Optional[str] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    username: str
    email: str
    is_admin: bool
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class Qna(UserBase):
    qna_id: int
    quiz_id: int
    question_text: str
    answer: int
    choice_1: str
    choice_2: str
    choice_3: str
    choice_4: str
