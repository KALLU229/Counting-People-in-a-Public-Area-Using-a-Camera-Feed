import jwt
from datetime import datetime, timedelta

SECRET_KEY = "change-this-secret-key"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MIN = 60

def create_token(email, role):
    payload = {
        "email": email,
        "role": role,
        "exp": datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MIN)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        return None
