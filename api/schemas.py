from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List, Tuple



# ---------- Users ----------
class UserBase(BaseModel):
    username:   str
    email:      str
    is_admin:   bool


class UserCreate(UserBase):
    username:   str
    email:      str
    is_admin:   bool
    password:   str


class UserUpdate(UserBase):
    username:   Optional[str] = None
    email:      Optional[str] = None
    is_admin:   Optional[str] = None
    password:   Optional[str] = None


class UserResponse(UserBase):
    username:   str
    email:      str
    is_admin:   bool
    id:         int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

        
# ---------- QnA ----------
class Qna(UserBase):
    qna_id:         int
    quiz_id:        int
    question_text:  str
    answer:         int
    choice_1:       str
    choice_2:       str
    choice_3:       str
    choice_4:       str


class QnaBase(BaseModel):
    question_text:  str
    choice_1:       str
    choice_2:       str
    choice_3:       str
    choice_4:       str
    answer:         int


# ---------- Quizzes ----------


# Schemas validering för Quizes-table
# obs! ex: class QuizBase(BaseModel) --> ARV!

# Gemensamma fält som alla versioner delar
class QuizBase(BaseModel):
    quiz_name:       str
    is_active:       bool
    number_question: int
    creator_id:      int

    questions: Optional[List[QnaBase]] = None


# Används: När man tar emot nya data(quiz) via POST -> IN till API:et
# pass <-- tomt kodblock, dvs vi lägger inte till något mer än det vi har ärvt
class QuizCreate(BaseModel):
    quiz_name:       str
    is_active:       Optional[bool] = True  # Default to True when creating
    number_question: int
    creator_id:      int 

# För framtida PUT/PATCH-endpoints (valfritt)
# Används: När du tar emot ÄNDRAD data via PUT/PATCH -> IN till API:et
class QuizUpdate(BaseModel):
    quiz_name:          Optional[str] = None
    is_active:          Optional[bool] = None
    number_question:    Optional[int] = None
    creator_id:         Optional[int] = None

# När man returnerar ett quiz från databasen
# Används: När du SKICKAR TILLBAKA quiz-data till klienten -> UT från API:et
class QuizResponse(QuizBase):
    id:             int
    is_active:      bool
    created_at:     datetime
    updated_at:     datetime

    class Config:
        from_attributes = True


class QuizResultBase(BaseModel):
    user_id:        int
    session_id:     int
    question_count: int
    score:          int
    taken_at:       Optional[datetime] = None
    time_taken:     int

class QuizResultCreate(QuizResultBase):
    pass

class QuizResultResponse(QuizResultBase):
    id: int

    class Config:
        orm_mode = True # "orm_mode = True" tells Pydantic to allow parsing data from ORM objects (like SQLAlchemy models), not just dicts.
        


# ---------- Submissions / Results ----------
class SubmissionRequest(BaseModel):
            pre_test:   dict[str, list[int]]
            post_test:  dict[str, list[int]]

class SubmissionResponse(BaseModel):
            n_users:            int
            question_per_user:  int
            pre_test_pct:       float
            post_test_pct:      float
            p_value:            float
            mean_improvement:   float
            std_improvement:    float
            cohens_d:           float
            t_stat:             float
