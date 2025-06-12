from pydantic import BaseModel, Field

class CartItemBase(BaseModel):
    product_id: int=Field(...,gt=0)
    quantity: int=Field(...,gt=0)

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    quantity: int=Field(...,gt=0)

class CartItemOut(CartItemBase):
    id: int

    class Config:
        orm_mode = True
