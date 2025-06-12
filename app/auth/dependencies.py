from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.auth.models import User
from app.core.config import ALGORITHM, SECRET_KEY
from app.core.database import get_db
from jose import JWTError, jwt

from app.exceptions.exception import InvalidCredentialsException

bearer_scheme = HTTPBearer()

#Check the current logged in userr
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),db: Session = Depends(get_db)) -> User:
    
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise InvalidCredentialsException
    except JWTError:
        raise InvalidCredentialsException

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise InvalidCredentialsException
    return user

#Check the logged in user is admin
def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return current_user

#check the logged in user role is user
def require_user(current_user:User = Depends(get_current_user)):
    if current_user.role != "user":
        raise HTTPException(status_code=403, detail="Users only")
    return current_user



