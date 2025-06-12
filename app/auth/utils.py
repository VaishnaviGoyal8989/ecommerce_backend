from passlib.context import CryptContext 
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.config import SECRET_KEY, ALGORITHM
import secrets
from app.auth import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_and_store_password_reset_token(db, user):
    token = secrets.token_urlsafe(32)  # Secure random token
    expiration = datetime.now(timezone.utc) + timedelta(minutes=5)

    reset_token = models.PasswordResetToken(
        user_id=user.id,
        token=token,
        expiration_time=expiration,
        used=False
    )
    db.add(reset_token)
    db.commit()
    db.refresh(reset_token)

    return token


def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=7)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password_reset_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            return None
        return email
    except jwt.JWTError:
        return None
