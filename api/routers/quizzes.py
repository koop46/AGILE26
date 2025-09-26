from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Quiz
from schemas import QuizCreate, QuizResponse, QuizUpdate
from typing import List


#ENDPOINTS - Dörrarna/Kommunikation
#OBS - response_model styr vad som skickas TILLBAKA från endpointen
# Ex: QuizCreate för att VALIDERA INKOMMANDE DATA
#     QuizResponse för att BETÄMMA HUR SVARET SKA SE UT


router = APIRouter(tags=["Quizzes"])



#för POST/quizzes --> Skapa nytt quiz
@router.post("/", response_model=QuizResponse)
def create_quiz(quiz: QuizCreate, db: Session = Depends(get_db)):    
    db_quiz = Quiz(**quiz.dict()) # <-- Vrf överstreckad?
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

#för GET/quizzes --> Hämta ALLA quiz
@router.get("/", response_model=List[QuizResponse])
def get_all_quizzes(db: Session = Depends(get_db)):
    return db.query(Quiz).all()


#för GET /quizzes/{quiz_id} –-> Hämta ett quiz via ID
@router.get("/{quiz_id}", response_model=QuizResponse)
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz


#för PUT /quizzes/{quiz_id} –-> Uppdatera quiz
@router.put("/{quiz_id}", response_model=QuizResponse)
def update_quiz(quiz_id: int, quiz_update: QuizUpdate, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    for key, value in quiz_update.dict(exclude_unset=True).items():
        setattr(quiz, key, value)

    db.commit()
    db.refresh(quiz)
    return quiz


#för DELETE /quizzes/{quiz_id} –-> Ta bort ett quiz
@router.delete("/{quiz_id}")
def delete_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    db.delete(quiz)
    db.commit()
    return {"detail": "Quiz deleted"}


