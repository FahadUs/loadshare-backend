# models/user_model.py

from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    user_type = Column(String, nullable=False)  # سنقيّدها بالقيم المسموحة لاحقاً
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        # ✅ تحديد القيم المسموحة فقط
        CheckConstraint(
            "user_type IN ('sender', 'receiver', 'driver', 'admin', 'support', 'vendor')",
            name="users_user_type_check"
        ),
    )
