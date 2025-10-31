# schemas/transaction_schema.py

from pydantic import BaseModel
from datetime import datetime

class TransactionBase(BaseModel):
    shipment_id: int
    payer_id: int
    amount: float
    payment_method: str
    status: str = "paid"

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
