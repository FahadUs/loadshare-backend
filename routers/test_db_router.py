from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user_model import User

router = APIRouter(
    prefix="/api/v1/test",
    tags=["DB Test"]
)

# ✅ READ ALL USERS
@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# ✅ INSERT TEST USER
@router.post("/insert")
def insert_test_user(db: Session = Depends(get_db)):
    try:
        test_user = User(
            name="Ahmad",
            phone="0599998800",
            email="crud.ahmad@loadshare.sa",
            password_hash="ues@no",
            user_type="driver"
        )
        print("🟢 STEP 2: Adding to DB session")
        db.add(test_user)

        print("🟢 STEP 3: Committing transaction...")
        db.commit()

        print("🟢 STEP 4: Refreshing object...")
        db.refresh(test_user)

        print(f"✅ STEP 5: User committed successfully: {test_user.id}")
        return {"message": "✅ Inserted", "id": test_user.id}

        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        return {"message": "✅ Inserted", "id": test_user.id}
    except Exception as e:
        import traceback
        traceback.print_exc()
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# ✅ DELETE USER BY EMAIL
@router.delete("/delete/{email}")
def delete_user(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": f"✅ User {email} deleted"}
