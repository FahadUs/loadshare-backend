# routers/vehicle_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.vehicle_model import Vehicle
from schemas.vehicle_schema import VehicleCreate, VehicleResponse

router = APIRouter(
    prefix="/api/v1/vehicles",
    tags=["Vehicles"]
)

# ✅ إضافة مركبة جديدة
@router.post("/create", response_model=VehicleResponse)
def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    try:
        new_vehicle = Vehicle(**vehicle.dict())
        db.add(new_vehicle)
        db.commit()
        db.refresh(new_vehicle)
        return new_vehicle
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating vehicle: {str(e)}")


# 🔍 استعراض جميع المركبات
@router.get("/", response_model=list[VehicleResponse])
def get_all_vehicles(db: Session = Depends(get_db)):
    vehicles = db.query(Vehicle).all()
    return vehicles


# 🔎 استعراض مركبة واحدة حسب ID
@router.get("/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle_by_id(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found.")
    return vehicle


# ❌ حذف مركبة
@router.delete("/{vehicle_id}")
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found.")
    db.delete(vehicle)
    db.commit()
    return {"message": f"Vehicle {vehicle_id} deleted successfully ✅"}
