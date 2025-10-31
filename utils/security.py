# utils/security.py

import bcrypt
from fastapi import HTTPException

def hash_password(password: str) -> str:
    try:
        # تأكد من أن كلمة السر لا تتجاوز الحد المسموح
        if len(password.encode("utf-8")) > 72:
            password = password[:72]

        # تحويل النص إلى bytes
        password_bytes = password.encode("utf-8")

        # توليد الملح
        salt = bcrypt.gensalt()

        # إنشاء التجزئة
        hashed = bcrypt.hashpw(password_bytes, salt)

        # إرجاع النص المشفر كـ string
        return hashed.decode("utf-8")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Password hashing failed: {str(e)}")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False
