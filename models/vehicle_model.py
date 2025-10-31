# models/vehicle_model.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Vehicle(Base):
    """
    Vehicle Model
    🔹 يمثل المركبة المسجلة في النظام.
    🔹 ترتبط بالمستخدم (السائق) عن طريق driver_id.
    """

    __tablename__ = "vehicles"

    # معرف المركبة (Primary Key)
    id = Column(Integer, primary_key=True, index=True)

    # السائق المسؤول عن المركبة
    driver_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # رقم اللوحة (فريد)
    plate_number = Column(String, unique=True, nullable=False)

    # نوع المركبة (شاحنة، سيارة نقل، تريلا...)
    type = Column(String, nullable=False)

    # السعة بالكيلوغرام أو الطن
    capacity = Column(Float, nullable=False)

    # حالة المركبة (متاحة، في مهمة، صيانة)
    status = Column(String, default="available")

    # تاريخ الإنشاء
    created_at = Column(DateTime, default=datetime.utcnow)

    # العلاقة العكسية مع المستخدم (السائق)
    driver = relationship("User", backref="vehicles")

