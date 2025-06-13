from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.auth.models import User
from app.core.config import ALGORITHM, SECRET_KEY
from app.core.database import get_db
from jose import JWTError, jwt
from app.core.logger import logger
from app.exceptions.exception import InvalidCredentialsException

bearer_scheme = HTTPBearer()

#Check the current logged in user
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),db: Session = Depends(get_db)) -> User:
    
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            logger.warning("JWT payload missing 'sub'")
            raise InvalidCredentialsException
        logger.info(f"Token decoded successfully for email: {email}")
    except JWTError:
        logger.error(f"JWT decoding failed")
        raise InvalidCredentialsException

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        logger.warning(f"No user found with email: {email}")
        raise InvalidCredentialsException
    logger.info(f"User authenticated: {user.email} (Role: {user.role})")
    return user

#Check the logged in user is admin
def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        logger.warning(f"Access denied: {User.email} is not an admin")
        raise HTTPException(status_code=403, detail="Admins only")
    logger.info(f"Admin access granted: {current_user.email}")
    return current_user

#check the logged in user role is user
def require_user(current_user:User = Depends(get_current_user)):
    if current_user.role != "user":
        logger.warning(f"Access denied: {current_user.email} is not a user")
        raise HTTPException(status_code=403, detail="Users only")
    logger.info(f"User access granted: {current_user.email}")
    return current_user



