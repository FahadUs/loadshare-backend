# schemas/feedback_schema.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FeedbackBase(BaseModel):
    shipment_id: int
    user_id: int
    rating: int
    comment: Optional[str] = None

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackResponse(FeedbackBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
