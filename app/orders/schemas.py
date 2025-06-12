from pydantic import BaseModel
from typing import List
from datetime import datetime


class OrderItemOut(BaseModel):
    product_id: int
    quantity: int
    price_at_purchase: float

    class Config:
        orm_mode = True

class OrderOut(BaseModel):
    id: int
    user_id: int
    total_amount: float
    created_at: datetime
    order_items: List[OrderItemOut]

    class Config:
        orm_mode = True