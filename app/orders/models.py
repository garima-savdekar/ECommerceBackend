import enum
from sqlalchemy import Column, DateTime, Integer, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class OrderStatus(str,enum.Enum):
    pending="pending"
    paid="paid"
    cancelled="cancelled"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_amount = Column(Float,nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending)
    created_at = Column(DateTime, default=datetime.now)

    user=relationship("User",back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "orderitems"

    id = Column(Integer, primary_key=True,index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer,nullable=False)
    price_at_purchase = Column(Float,nullable=False)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product",back_populates="orderitems")