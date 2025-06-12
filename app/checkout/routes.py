from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.dependencies import require_user
from app.checkout import crud
from app.exceptions.exception import EmptyCartException
from app.orders.schemas import OrderOut
from app.core.logger import logger


router = APIRouter(prefix="/checkout", tags=["Checkout"])

#API to make order and delete items from cart
@router.post("/", response_model=OrderOut)
def checkout(db: Session = Depends(get_db), user=Depends(require_user)):
    logger.info(f"User {user.id} initiated checkout")

    try:
        order = crud.perform_checkout(db, user.id)
    except ValueError as e:
        logger.error(f"Checkout error for user {user.id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    if not order:
        logger.warning(f"Checkout failed — empty cart for user {user.id}")
        raise EmptyCartException()

    logger.info(f"Checkout successful — Order ID {order.id} created for user {user.id}")
    return order
