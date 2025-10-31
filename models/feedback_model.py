# models/feedback_model.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Feedback(Base):
    """
    Feedback Model
    🔹 يمثل تقييم المستخدم بعد إتمام الشحنة.
    🔹 كل تقييم مرتبط بشحنة واحدة ومستخدم واحد.
    """

    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)

    # الشحنة اللي تم تقييمها
    shipment_id = Column(Integer, ForeignKey("shipments.id"), nullable=False)

    # المستخدم اللي كتب التقييم (client / driver)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # التقييم (من 1 إلى 5)
    rating = Column(Integer, nullable=False)

    # تعليق اختياري
    comment = Column(String, nullable=True)

    # وقت إنشاء التقييم
    created_at = Column(DateTime, default=datetime.utcnow)

    # العلاقات
    shipment = relationship("Shipment", backref="feedbacks")
    user = relationship("User", backref="user_feedbacks")
