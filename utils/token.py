from datetime import datetime, timedelta
from jose import JWTError, jwt

# المفتاح السري لتوليد التوكن
SECRET_KEY = "your_secret_key_here"  # 🔐 غيّرها لاحقاً بقيمة بيئية
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # صلاحية التوكن بالوقت (دقيقة)

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    إنشاء JWT Token بعد تسجيل الدخول الناجح
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    """
    التحقق من صحة التوكن عند كل طلب محمي
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
