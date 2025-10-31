from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user_model import User
from utils.security import verify_password
from utils.token import create_access_token

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

@router.post("/login")
def login_user(email: str, password: str, db: Session = Depends(get_db)):
    """
    تسجيل الدخول باستخدام البريد الإلكتروني وكلمة المرور
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # إنشاء التوكن
    token = create_access_token({"sub": user.email, "role": user.user_type})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_role": user.user_type
    }
