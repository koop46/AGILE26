from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey
from database import Base
from datetime import datetime, timezone
from sqlalchemy.orm import relationship #added relationship import /Einar


class User(Base):

    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    quiz_results = relationship("QuizResult", back_populates="user")


class Question(Base):
    __tablename__ = "questions"

    qna_id = Column(Integer, primary_key=True, nullable=False)
    quiz_id = Column(Integer, nullable=False)
    question_text = Column(String, nullable=False)

    choice_1 = Column(String, nullable=False)
    choice_2 = Column(String, nullable=False)
    choice_3 = Column(String, nullable=False)
    choice_4 = Column(String, nullable=False)

    answer = Column(Integer, nullable=False)


class Quiz(Base):

    __tablename__ = 'quizzes'

    id = Column(Integer, primary_key=True)
    quiz_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    number_question = Column(Integer, nullable=False)
    creator_id = Column(Integer, nullable=False)  # ev. ForeignKey till User.id senare
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    quiz_results = relationship("QuizResult", back_populates="quiz")

"""
Each row represents a user's attempt at a given quiz.
Multiple rows may therefore reference the same session and quiz but be for different users.

Fields for QuizResult:
- id: Primary key for the quiz result entry.
- user_id: Foreign key referencing the User who took the quiz.
- session_id: An optional field to track the session in which the quiz was taken.
- question_count: The total number of questions in the quiz.
- score: The amount of correct answers the user achieved on the quiz.


- time_taken: The time taken by the user to complete the quiz (in seconds).
- timestamp: The date and time when the quiz was taken.
- user: Relationship to the User model.
- quiz: Relationship to the Quiz model. 


"""


class QuizResult(Base): 

    __tablename__   = 'quiz_results'

    id              = Column(Integer, primary_key=True)
    user_id         = Column(Integer, ForeignKey('users.id'), nullable=False)
    session_id      = Column(Integer, ForeignKey('session.id'), nullable=False)
    question_count  = Column(Integer, nullable=False)
    score           = Column(Integer, nullable=False) 

    # Keep in mind we need to calculate score for to log answers in this way 
    # It might be better to log answers and calculate score after?
    

    taken_at        = Column(DateTime, default=datetime.utcnow) #instead of timestamp we use taken_at
    time_taken      = Column(Integer, nullable=False)  # Time taken in seconds 
    user            = relationship("User", back_populates="quiz_results")
    quiz            = relationship("Quiz", back_populates="quiz_results")