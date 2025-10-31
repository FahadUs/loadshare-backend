# schemas/shipment_schema.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ShipmentBase(BaseModel):
    sender_id: int
    receiver_id: int
    driver_id: Optional[int]
    vehicle_id: Optional[int]
    origin: str
    destination: str
    weight: Optional[float]
    cost: float
    status: Optional[str] = "pending"

class ShipmentCreate(ShipmentBase):
    pass

class ShipmentResponse(ShipmentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
