from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import get_db
from api.schemas import SubmissionRequest, SubmissionResponse
from api.kirkpatrick import KirkpatrickModel


#from api.models import Quiz
#from typing import List

router = APIRouter(
    tags=["submission"]
)
 
@router.post("/submit_answers", response_model=SubmissionResponse)
def submit_answers(submission: SubmissionRequest, db: Session = Depends(get_db)):

    if not submission.pre_test or not submission.post_test:
        raise HTTPException(status_code=404, detail="Pre-or post-test not found")

    evaluator = KirkpatrickModel(submission.pre_test, submission.post_test)
    summary = evaluator.summary()

    return summary
