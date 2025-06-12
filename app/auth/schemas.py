from pydantic import BaseModel, EmailStr, Field, field_validator
from app.auth import models
from app.utils.utils import validate_strong_password

class UserCreate(BaseModel):
    name: str=Field(...,min_length=1)
    email: EmailStr
    password: str
    role: models.RoleEnum = models.RoleEnum.user

    @field_validator("password")
    def validate_password(cls, value):
        return validate_strong_password(value)

class UserSignin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    class Config:
        orm_mode = True
   
class ForgotPassword(BaseModel):
    email:EmailStr

class ResetPassword(BaseModel):
    token:str
    new_password: str

    @field_validator("new_password")
    def validate_new_password(cls, value):
        return validate_strong_password(value)
