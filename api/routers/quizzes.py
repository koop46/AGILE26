from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import get_db
from api.models import Quiz, Question
from api.schemas import QuizCreate, QuizResponse, QuizUpdate, QnaBase
from typing import List


#ENDPOINTS - Dörrarna/Kommunikation
#OBS - response_model styr vad som skickas TILLBAKA från endpointen
# Ex: QuizCreate för att VALIDERA INKOMMANDE DATA
#     QuizResponse för att BETÄMMA HUR SVARET SKA SE UT


router = APIRouter(tags=["Quizzes"])



#för POST/quizzes --> Skapa nytt quiz
@router.post("/", response_model=QuizResponse)
def create_quiz(quiz: QuizCreate, db: Session = Depends(get_db)):    
    # Filter out any fields that don't belong in the Quiz model
    quiz_data = quiz.dict()
    # Remove questions field if it exists (it's handled separately)
    quiz_data.pop('questions', None)
    
    db_quiz = Quiz(**quiz_data)
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


#för POST /quizzes/{quiz_id}/questions –-> Lägg till fråga till quiz
@router.post("/{quiz_id}/questions")
def add_question_to_quiz(quiz_id: int, question: QnaBase, db: Session = Depends(get_db)):
    # Check if quiz exists
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Create new question
    db_question = Question(
        quiz_id=quiz_id,
        question_text=question.question_text,
        choice_1=question.choice_1,
        choice_2=question.choice_2,
        choice_3=question.choice_3,
        choice_4=question.choice_4,
        answer=question.answer
    )
    
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    
    return {"detail": "Question added successfully", "question_id": db_question.qna_id}

@router.delete("/{quiz_id}/questions")
def delete_quiz_questions(quiz_id: int, db: Session = Depends(get_db)):
    """Delete all questions for a specific quiz"""
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Delete all questions for this quiz
    db.query(Question).filter(Question.quiz_id == quiz_id).delete()
    db.commit()
    
    return {"detail": "All questions deleted successfully"}


