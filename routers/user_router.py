from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from database import get_db
from models.user_model import User
from schemas.user_schema import UserCreate, UserResponse
from utils.security import hash_password

# ✅ تعريف الراوتر لازم يكون أول شيء قبل أي @router.post
router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"]
)

@router.post("/register", response_model=UserResponse)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    print("🟢 STEP 1: Payload received:", payload.dict())

    existing_user = db.query(User).filter(
        or_(
            User.email == payload.email,
            User.phone == payload.phone
        )
    ).first()

    print("🟢 STEP 2: Existing user check done")

    if existing_user:
        print("🔴 STEP 3: User already exists")
        raise HTTPException(status_code=400, detail="User already exists with this email or phone.")

    # نحاول تشفير كلمة المرور
    try:
        print("🟢 STEP 4: Hashing password...")
        hashed_pw = hash_password(payload.password)
        print("🟢 STEP 5: Password hashed successfully:", hashed_pw[:30])
    except Exception as e:
        import traceback
        print("❌ ERROR in hashing:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Password hashing failed: {str(e)}")

    new_user = User(
        name=payload.name,
        phone=payload.phone,
        email=payload.email,
        password_hash=hashed_pw,
        user_type=payload.user_type
    )

    print("🟢 STEP 6: User object created")

    try:
        print("🟢 STEP 6.1: Adding user to DB session")
        db.add(new_user)
        print("🟢 STEP 6.2: Committing changes...")
        db.commit()
        print("🟢 STEP 6.3: Refreshing user...")
        db.refresh(new_user)
        print("✅ STEP 7: User committed successfully:", new_user.id)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("❌ ERROR during DB commit:", str(e))
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    print("✅ STEP 8: Registration completed successfully")
    return new_user
