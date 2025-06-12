import uuid
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import HTTPException
from app.auth.models import PasswordResetToken
from sqlalchemy.orm import Session
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
from app.core.logger import logger

load_dotenv()

EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return context.verify(plain, hashed)

#Create the token for logged in user
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#Create reset token for password reset
def create_reset_token(db: Session, user_id: int) -> str:
    token = str(uuid.uuid4())
    expiration = datetime.now(timezone.utc) + timedelta(minutes=15)
    reset_token = PasswordResetToken(
        user_id=user_id,
        token=token,
        expiration_time=expiration,
        used=False
    )
    db.add(reset_token)
    db.commit()
    db.refresh(reset_token)
    return token

#verify token for reset password
def verify_reset_token(db: Session, token: str) -> PasswordResetToken:
    record = db.query(PasswordResetToken).filter_by(token=token, used=False).first()
    if not record:
        raise HTTPException(status_code=400, detail="Invalid or expired token.")
    
    if record.expiration_time.tzinfo is None:
        record_expiration = record.expiration_time.replace(tzinfo=timezone.utc)
    else:
        record_expiration = record.expiration_time

    if record_expiration < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Token has expired.")
    
    return record

#Mark token used after using the token for password change
def mark_token_used(db: Session, token_record: PasswordResetToken):
    token_record.used = True
    db.commit()

#Function to send the email to user for password reset
def send_reset_email(email: str, token: str) -> str:
    reset_link = f"http://localhost:8000/auth/reset-password?token={token}"
    subject = "Reset Your Password"
    body = f"""
    Hi,
    You requested a password reset. 
    Click the link below to reset your password:
    {reset_link}
    This link will expire in 15 minutes.
    If you didn't request this, please ignore this email.

    - Your App Team
    """

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = email
    msg.set_content(body)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_FROM, EMAIL_PASSWORD)
            smtp.send_message(msg)
        logger.info(f"Password reset email sent to: {email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
        logger.error(f"Failed to send reset email to {email}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to send reset email.")

    return reset_link

