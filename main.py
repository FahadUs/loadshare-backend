from fastapi import FastAPI
from fastapi import FastAPI
from database import Base, engine
from routers import user_router, test_db_router, shipment_router, vehicle_router, transaction_router, feedback_router, auth_router
from models import (
    user_model,
    vehicle_model,
    shipment_model,
    transaction_model,
    feedback_model
)





app = FastAPI(title="LoadShare API")

Base.metadata.create_all(bind=engine)

# ✅ إضافة الراوتر هنا قبل أي دوال
app.include_router(user_router.router)
app.include_router(test_db_router.router)
app.include_router(shipment_router.router)
app.include_router(vehicle_router.router)
app.include_router(transaction_router.router)
app.include_router(feedback_router.router)
app.include_router(auth_router.router)


@app.get("/")
def root():
    return {"message": "LoadShare Backend is running 🚛"}
