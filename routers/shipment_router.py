# routers/shipment_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.shipment_model import Shipment
from schemas.shipment_schema import ShipmentCreate, ShipmentResponse
from utils.dependencies import get_current_user
from models.user_model import User

router = APIRouter(
    prefix="/api/v1/shipments",
    tags=["Shipments"]
)

# 🟢 إنشاء شحنة جديدة
@router.post("/create", response_model=ShipmentResponse)
def create_shipment(
        shipment: ShipmentCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):

    try:
        print(f"✅ Authorized user: {current_user.email} ({current_user.user_type})")

        new_shipment = Shipment(**shipment.dict())
        db.add(new_shipment)
        db.commit()
        db.refresh(new_shipment)
        return new_shipment
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating shipment: {str(e)}")


# 🔵 استعراض جميع الشحنات
@router.get("/", response_model=list[ShipmentResponse])
def get_all_shipments(db: Session = Depends(get_db)):
    shipments = db.query(Shipment).all()
    return shipments


# 🟠 استعراض شحنة محددة عبر ID
@router.get("/{shipment_id}", response_model=ShipmentResponse)
def get_shipment_by_id(shipment_id: int, db: Session = Depends(get_db)):
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found.")
    return shipment


# 🔴 حذف شحنة محددة
@router.delete("/{shipment_id}")
def delete_shipment(
        shipment_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found.")
    db.delete(shipment)
    db.commit()
    return {"message": f"Shipment {shipment_id} deleted successfully ✅"}
