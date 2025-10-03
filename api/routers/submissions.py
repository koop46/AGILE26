from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import SubmissionRequest, SubmissionResponse
from kirkpatrick import KirkpatrickModel

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
