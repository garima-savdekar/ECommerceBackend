from sqlalchemy import Column, Integer, String, Enum ,Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum
from datetime import datetime, timedelta, timezone

class RoleEnum(str, enum.Enum):
    admin = "admin"
    user = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password= Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default="user")

    reset_tokens=relationship("PasswordResetToken",back_populates="user")
    cartitems=relationship("Cart",back_populates="user")
    orders=relationship("Order",back_populates="user")
    products = relationship("Product", back_populates="admin")


class PasswordResetToken(Base):
    __tablename__ = "passwordresettokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, unique=True, nullable=False)
    expiration_time = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc) + timedelta(minutes=15))
    used = Column(Boolean, default=False)

    user = relationship("User", back_populates="reset_tokens")