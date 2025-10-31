# schemas/vehicle_schema.py

from pydantic import BaseModel
from datetime import datetime

class VehicleBase(BaseModel):
    driver_id: int
    plate_number: str
    type: str
    capacity: float
    status: str = "available"

class VehicleCreate(VehicleBase):
    pass

class VehicleResponse(VehicleBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
