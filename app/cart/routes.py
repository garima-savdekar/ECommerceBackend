from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.auth.dependencies import require_user
from app.cart import schemas, crud
from app.exceptions.exception import CartItemNotFoundException, EmptyCartException
from app.core.logger import logger

router = APIRouter(prefix="/cart", tags=["Cart"])

#Add item in cart api
@router.post("/", response_model=schemas.CartItemOut)
def add_item(item: schemas.CartItemCreate, db: Session = Depends(get_db), user=Depends(require_user)):
    logger.info(f"User {user.id} adding product {item.product_id} to cart (Quantity: {item.quantity})")
    return crud.add_to_cart(db, user_id=user.id, item=item)

#API to view the cart items
@router.get("/", response_model=List[schemas.CartItemOut])
def view_cart(db: Session = Depends(get_db), user=Depends(require_user)):
    cart_items = crud.get_user_cart(db, user_id=user.id)
    if not cart_items:
        logger.warning(f"User {user.id} has an empty cart")
        raise EmptyCartException()
    logger.info(f"User {user.id} viewing cart with {len(cart_items)} items")
    return cart_items
    
#API to update the already existing cart item
@router.put("/{product_id}", response_model=schemas.CartItemOut)
def update_cart(product_id: int, data: schemas.CartItemUpdate, db: Session = Depends(get_db), user=Depends(require_user)):
    updated = crud.update_cart_item(db, user_id=user.id, product_id=product_id, quantity=data.quantity)
    if not updated:
        logger.error(f"User {user.id} tried updating non-existent cart item: Product ID {product_id}")
        raise CartItemNotFoundException(product_id)
    logger.info(f"User {user.id} updated product {product_id} quantity to {data.quantity} in cart")
    return updated

#API to delete the cart item
@router.delete("/{product_id}")
def delete_item(product_id: int, db: Session = Depends(get_db), user=Depends(require_user)):
    removed = crud.remove_cart_item(db, user_id=user.id, product_id=product_id)
    if not removed:
        logger.error(f"User {user.id} tried to delete non-existent cart item: Product ID {product_id}")
        raise CartItemNotFoundException(product_id)
    logger.info(f"User {user.id} removed product {product_id} from cart")
    return {"message": "Item removed from cart"}