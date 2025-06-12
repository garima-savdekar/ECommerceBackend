from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock = Column(Integer)
    category = Column(String)
    image_url = Column(String)
    admin_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    orderitems=relationship("OrderItem",back_populates="product")
    cartitems=relationship("Cart",back_populates="product")
    admin = relationship("User", back_populates="products")
