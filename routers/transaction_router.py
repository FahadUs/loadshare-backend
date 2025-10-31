# routers/transaction_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.transaction_model import Transaction
from schemas.transaction_schema import TransactionCreate, TransactionResponse

router = APIRouter(
    prefix="/api/v1/transactions",
    tags=["Transactions"]
)

# ✅ إنشاء عملية دفع جديدة
@router.post("/create", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    try:
        new_transaction = Transaction(**transaction.dict())
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)
        return new_transaction
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating transaction: {str(e)}")


# 🔍 عرض جميع العمليات
@router.get("/", response_model=list[TransactionResponse])
def get_all_transactions(db: Session = Depends(get_db)):
    transactions = db.query(Transaction).all()
    return transactions


# 🔎 عرض عملية محددة برقمها
@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction_by_id(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found.")
    return transaction


# ❌ حذف عملية دفع
@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found.")
    db.delete(transaction)
    db.commit()
    return {"message": f"Transaction {transaction_id} deleted successfully ✅"}
