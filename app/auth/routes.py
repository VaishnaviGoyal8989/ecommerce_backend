from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.auth import schemas, utils, models, email_utils
from jose import JWTError, jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timezone
from app.utils.dependency import get_db

import logging
logger = logging.getLogger("ecommerce_logger")

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", status_code=201)
def signup(data: schemas.Signup, db: Session = Depends(get_db)):
    try:
        if db.query(models.User).filter_by(email=data.email).first():
            logger.warning(f"Signup failed: Email already exists - {data.email}")
            raise HTTPException(status_code=400, detail="Email already exists")

        hashed_pw = utils.hash_password(data.password)
        user = models.User(name=data.name, email=data.email, hashed_password=hashed_pw, role=data.role)
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"User signed up successfully - {data.email}")
        return {"message": "User created successfully"}
    
    except HTTPException as http_exc:
         raise http_exc
    
    except Exception as e:
        logger.error(f"Signup error: {str(e)}")
        raise HTTPException(status_code=500, detail="Something went wrong during signup")

@router.post("/signin", response_model=schemas.Token)
def signin(data: schemas.Signin, db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter_by(email=data.email).first()
        if not user or not utils.verify_password(data.password, user.hashed_password):
            logger.warning(f"Signin failed: Invalid credentials for {data.email}")
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = utils.create_access_token(data={"sub": user.email, "role": user.role})
        refresh_token = utils.create_refresh_token(data={"sub": user.email})
        logger.info(f"User signed in: {data.email}")
        return {"access_token": access_token, "refresh_token": refresh_token}
    
    except HTTPException as http_exc:
         raise http_exc
    
    except Exception as e:
        logger.error(f"Signin error for {data.email}: {str(e)}")
        raise HTTPException(status_code=500, detail="Something went wrong during signin")

@router.post("/refresh", response_model=schemas.Token)
def refresh_token(data: schemas.RefreshTokenRequest):
    try:
        payload = jwt.decode(data.refresh_token, utils.SECRET_KEY, algorithms=[utils.ALGORITHM])
        email = payload.get("sub")
        if not email:
            logger.warning("Refresh token missing subject")
            raise HTTPException(status_code=401, detail="Invalid token")

        access_token = utils.create_access_token(data={"sub": email})
        new_refresh_token = utils.create_refresh_token(data={"sub": email})
        logger.info(f"Refresh token success for {email}")
        return {"access_token": access_token, "refresh_token": new_refresh_token}
    
    except JWTError:
        logger.warning("Invalid refresh token")
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        raise HTTPException(status_code=500, detail="Something went wrong during token refresh")

@router.post("/forgot-password")
def forgot_password(data: schemas.ForgotPasswordRequest, db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter_by(email=data.email).first()
        if not user:
            logger.warning(f"Forgot password: Email not found - {data.email}")
            raise HTTPException(status_code=404, detail="Email not found. Please check and try again.")

        reset_token = utils.create_and_store_password_reset_token(db, user)
        email_utils.send_reset_email(user.email, reset_token)
        logger.info(f"Reset token sent to {user.email}")
        return {"message": "If the email is registered, a reset token has been sent to your email."}
    
    except HTTPException as http_exc:
         raise http_exc
    
    except Exception as e:
        logger.error(f"Forgot password error for {data.email}: {str(e)}")
        raise HTTPException(status_code=500, detail="Something went wrong during forgot password")

@router.post("/reset-password")
def reset_password(data: schemas.ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        db_token = db.query(models.PasswordResetToken).filter_by(token=data.token).first()
        if not db_token:
            logger.warning("Reset password: Invalid token")
            raise HTTPException(status_code=400, detail="Invalid token")
        if db_token.used:
            logger.warning("Reset password: Token already used")
            raise HTTPException(status_code=400, detail="Token already used")
        if db_token.expiration_time.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            logger.warning("Reset password: Token expired")
            raise HTTPException(status_code=400, detail="Token expired")

        user = db_token.user
        hashed_pw = utils.hash_password(data.new_password)
        user.hashed_password = hashed_pw
        db_token.used = True
        db.commit()
        logger.info(f"Password reset successful for {user.email}")
        return {"message": "Password reset successful"}
    
    except HTTPException as http_exc:
         raise http_exc
    
    except Exception as e:
        logger.error(f"Reset password error: {str(e)}")
        raise HTTPException(status_code=500, detail="Something went wrong during password reset")
