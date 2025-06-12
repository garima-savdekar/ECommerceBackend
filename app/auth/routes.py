from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, get_db
from app.auth.schemas import UserCreate,UserOut,UserSignin,ForgotPassword, ResetPassword, Token
from app.exceptions.exception import DuplicateEmailException, InvalidCredentialsException, UserNotFoundException
from app.auth.utils import create_reset_token, hash_password, mark_token_used,verify_password,create_access_token, verify_reset_token, send_reset_email
from app.auth.models import User
from app.core.logger import logger

router = APIRouter(prefix="/auth", tags=["Authentication"])

#API for registration of new user
@router.post("/signup", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):

    if db.query(User).filter(User.email == user.email).first():
        logger.warning(f"Signup failed Duplicate email: {user.email}")
        raise DuplicateEmailException(user.email)

    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"User registered successfully: {user.email} | Role: {user.role}")
    return new_user

#API for log in the user
@router.post("/signin",response_model=Token)
def login(form: UserSignin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.email).first()

    if not user or not verify_password(form.password, user.hashed_password):
        logger.warning(f"Failed login: {form.email}")
        raise InvalidCredentialsException()
    
    tokenstr = create_access_token(data={"sub": user.email, "role": user.role})
    token=Token(access_token=tokenstr)
    logger.info(f"Successful login: {user.email} | Role: {user.role}")
    return token

#Forgot password api which will send email
@router.post("/forgot-password",response_model=dict)
def forgot_password(data: ForgotPassword, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        logger.warning(f"Forgot password failed - Email not found: {data.email}")
        raise UserNotFoundException()

    token = create_reset_token(db, user.id)
    send_reset_email(user.email, token)
    logger.info(f"Password reset token generated and emailed to: {user.email}")
    return {"message": "Password reset token sent to email."}

#Reset password api 
@router.post("/reset-password",response_model=dict)
def reset_password(data: ResetPassword, db: Session = Depends(get_db)):
    
    token_record = verify_reset_token(db, data.token)
    user = db.query(User).filter(User.id == token_record.user_id).first()
    if not user:
        logger.warning(f"Reset password failed user not found")
        raise UserNotFoundException()
    
    user.hashed_password = hash_password(data.new_password)
    mark_token_used(db, token_record)
    db.commit()
    logger.info(f"Password reset successful for user ID: {user.id} | Email: {user.email}")
    return {"message": "Password has been reset successfully."}
   

