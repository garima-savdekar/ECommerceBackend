from sqlalchemy import Column,Integer,ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Cart(Base):
    __tablename__="cart"

    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"))
    product_id=Column(Integer,ForeignKey("products.id"))
    quantity=Column(Integer,default=1)

    user=relationship("User",back_populates="cartitems")
    product=relationship("Product",back_populates="cartitems")