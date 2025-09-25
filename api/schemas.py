from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List, Tuple

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

class QnaBase(BaseModel):
    question_text: str
    choice_1: str
    choice_2: str
    choice_3: str
    choice_4: str
    answer: int

class QuizBase(BaseModel):
    quiz_name: str
    number_question: int
    creator_id: int

    questions: Optional[List[QnaBase]] = None


# Används: När man tar emot nya data(quiz) via POST -> IN till API:et
# pass <-- tomt kodblock, dvs vi lägger inte till något mer än det vi har ärvt
class QuizCreate(QuizBase):
    pass 

# För framtida PUT/PATCH-endpoints (valfritt)
# Används: När du tar emot ÄNDRAD data via PUT/PATCH -> IN till API:et
class QuizUpdate(BaseModel):
    quiz_name: Optional[str] = None
    number_question: Optional[int] = None
    creator_id: Optional[int] = None

# När man returnerar ett quiz från databasen
# Används: När du SKICKAR TILLBAKA quiz-data till klienten -> UT från API:et
class QuizResponse(QuizBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True