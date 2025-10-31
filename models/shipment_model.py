# models/shipment_model.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Shipment(Base):
    """
    Shipment Model
    🔹 يمثل عملية شحن بين المرسل والمستقبل.
    🔹 يربط المستخدمين (المرسل، المستقبل، السائق) بالمركبة.
    """

    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)

    # المرسل والمستقبل والسائق
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # المركبة المستخدمة
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)

    # معلومات الرحلة
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    weight = Column(Float)
    cost = Column(Float, nullable=False)

    # حالة الشحنة
    status = Column(String, default="pending")  # pending, assigned, in_transit, delivered

    # وقت الإنشاء
    created_at = Column(DateTime, default=datetime.utcnow)

    # العلاقات (اختيارية حالياً)
    sender = relationship("User", foreign_keys=[sender_id], backref="sent_shipments")
    receiver = relationship("User", foreign_keys=[receiver_id], backref="received_shipments")
    driver = relationship("User", foreign_keys=[driver_id], backref="driving_shipments")
    vehicle = relationship("Vehicle", backref="shipments")
