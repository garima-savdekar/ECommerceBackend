from sqlalchemy.orm import Session
from app.cart import models, schemas
from app.exceptions.exception import ProductNotFoundException
from app.products.models import Product

#Function to get user cart 
def get_user_cart(db: Session, user_id: int):
    return db.query(models.Cart).filter(models.Cart.user_id == user_id).all()

#for adding prodcuts in cart
def add_to_cart(db: Session, user_id: int, item: schemas.CartItemCreate):

    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise ProductNotFoundException()
    
    existing = db.query(models.Cart).filter_by(user_id=user_id, product_id=item.product_id).first()

    if existing:
        existing.quantity += item.quantity
        db.commit()
        db.refresh(existing)
        return existing

    cart_item = models.Cart(user_id=user_id, product_id=item.product_id, quantity=item.quantity)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item

#Update the already existing cart item
def update_cart_item(db: Session, user_id: int, product_id: int, quantity: int):
    item = db.query(models.Cart).filter_by(user_id=user_id, product_id=product_id).first()
    
    if item:
        item.quantity = quantity
        db.commit()
        db.refresh(item)
        return item
    return None

#Remove the item from cart
def remove_cart_item(db: Session, user_id: int, product_id: int):
    item = db.query(models.Cart).filter_by(user_id=user_id, product_id=product_id).first()
    if item:
        db.delete(item)
        db.commit()
        return True
    return False