from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey
from api.database import Base
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

# ---------------- Users ----------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    #  Lazy loading optimization
    quiz_results = relationship("QuizResult", back_populates="user", lazy="selectin")


# ---------------- Quizzes & Questions ----------------
class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True)
    quiz_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    number_question = Column(Integer, nullable=False)
    creator_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    #  Faster joins using selectin
    quiz_results = relationship("QuizResult", back_populates="quiz", lazy="selectin")
    questions = relationship("Question", back_populates="quiz",
                             cascade="all, delete-orphan", lazy="selectin")


class Question(Base):
    __tablename__ = "questions"

    qna_id = Column(Integer, primary_key=True, nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    question_text = Column(String, nullable=False)

    choice_1 = Column(String, nullable=False)
    choice_2 = Column(String, nullable=False)
    choice_3 = Column(String, nullable=False)
    choice_4 = Column(String, nullable=False)

    answer = Column(Integer, nullable=False)

    # Load related quiz efficiently
    quiz = relationship("Quiz", back_populates="questions", lazy="selectin")


# ---------------- Sessions ----------------
class AppSession(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    #  Load all quiz results in one go when needed
    quiz_results = relationship("QuizResult", back_populates="session", lazy="selectin")


# ---------------- Quiz Results ----------------
class QuizResult(Base):
    __tablename__ = "quiz_results"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=True)

    question_count = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)
    taken_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    time_taken = Column(Integer, nullable=False)

    #  Add lazy="selectin" everywhere for efficient joins
    user = relationship("User", back_populates="quiz_results", lazy="selectin")
    quiz = relationship("Quiz", back_populates="quiz_results", lazy="selectin")
    session = relationship("AppSession", back_populates="quiz_results", lazy="selectin")
