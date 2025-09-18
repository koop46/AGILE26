from sqlalchemy import Boolean, Column, DateTime, Integer, String
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


# Quizzes-table - fält för tabellen
class Quiz(Base):

    __tablename__ = 'quizzes'

    id = Column(Integer, primary_key=True)
    quiz_name = Column(String, nullable=False)
    number_question = Column(Integer, nullable=False)
    creator_id = Column(Integer, nullable=False)  # ev. ForeignKey till User.id senare
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


