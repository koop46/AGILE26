from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey
from database import Base
from datetime import datetime, timezone

class User(Base):

    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class Question(Base):
    __tablename__ = "questions"

    qna_id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey("quiz.quiz_id"), nullable=False)
    question_text = Column(String, nullable=False)

    choice_1 = Column(String, nullable=False)
    choice_2 = Column(String, nullable=False)
    choice_3 = Column(String, nullable=False)
    choice_4 = Column(String, nullable=False)

    answer = Column(Integer, nullable=False)
    
