# models/transaction_model.py

from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Transaction(Base):
    """
    Transaction Model
    🔹 يمثل دفعة (فاتورة) مرتبطة بشحنة.
    🔹 يخزن المبلغ، طريقة الدفع، وحالة الدفع.
    """

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    # الشحنة اللي تخص هذه العملية
    shipment_id = Column(Integer, ForeignKey("shipments.id"), nullable=False)

    # الشخص الدافع (Who paid? غالباً المرسل أو العميل)
    payer_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # كم دفع؟
    amount = Column(Float, nullable=False)

    # طريقة الدفع (كاش / تحويل / بطاقة / محفظة)
    payment_method = Column(String, nullable=False)  # "cash", "card", "bank", ...

    # حالة الدفع
    status = Column(String, default="paid")  # "paid", "pending", "failed", "refunded"

    created_at = Column(DateTime, default=datetime.utcnow)

    # علاقات (عشان تقدر تتبع الدفع من البايثون بدون سؤال SQL يدوي)
    shipment = relationship("Shipment", backref="transactions")
    payer = relationship("User", backref="transactions_made")
