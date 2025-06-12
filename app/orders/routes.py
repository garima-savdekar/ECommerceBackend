from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.auth.dependencies import require_user
from app.exceptions.exception import OrderNotFoundException
from app.orders import schemas, crud
from app.core.logger import logger

router = APIRouter(prefix="/orders", tags=["Orders"])

#Get the order history of user
@router.get("", response_model=List[schemas.OrderOut])
def get_order_history(db: Session = Depends(get_db), user=Depends(require_user)):
    logger.info(f"User {user.id} requested their order history")
    orders=crud.get_user_orders(db, user.id)
    logger.info(f"User {user.id} has {len(orders)} orders")
    return orders

#Get only the deatil of particular order
@router.get("/{order_id}", response_model=schemas.OrderOut)
def get_order_detail(order_id: int, db: Session = Depends(get_db), user=Depends(require_user)):
    logger.info(f"User {user.id} requested details for order ID: {order_id}")
    order = crud.get_order_by_id(db, order_id, user.id)
    if not order:
        logger.warning(f"Order ID {order_id} not found for user {user.id}")
        raise OrderNotFoundException(order_id)
    logger.info(f"Order ID {order_id} returned to user {user.id}")
    return order