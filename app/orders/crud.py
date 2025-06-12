from sqlalchemy.orm import Session
from app.orders.models import Order

#Get the orders for particular user
def get_user_orders(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).order_by(Order.created_at.desc()).all()

#Retrieve the order of given id
def get_order_by_id(db: Session, order_id: int, user_id: int):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
    return order