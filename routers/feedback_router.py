# routers/feedback_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.feedback_model import Feedback
from schemas.feedback_schema import FeedbackCreate, FeedbackResponse

router = APIRouter(
    prefix="/api/v1/feedbacks",
    tags=["Feedbacks"]
)


# ✅ إنشاء تقييم جديد
@router.post("/create", response_model=FeedbackResponse)
def create_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    try:
        new_feedback = Feedback(**feedback.dict())
        db.add(new_feedback)
        db.commit()
        db.refresh(new_feedback)
        return new_feedback
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating feedback: {str(e)}")


# 🔍 عرض جميع التقييمات
@router.get("/", response_model=list[FeedbackResponse])
def get_all_feedbacks(db: Session = Depends(get_db)):
    feedbacks = db.query(Feedback).all()
    return feedbacks


# 🔎 عرض تقييم معين
@router.get("/{feedback_id}", response_model=FeedbackResponse)
def get_feedback_by_id(feedback_id: int, db: Session = Depends(get_db)):
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found.")
    return feedback


# ❌ حذف تقييم
@router.delete("/{feedback_id}")
def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found.")
    db.delete(feedback)
    db.commit()
    return {"message": f"Feedback {feedback_id} deleted successfully ✅"}
