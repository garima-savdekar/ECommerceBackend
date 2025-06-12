from sqlalchemy.orm import Session
from app.exceptions.exception import ItemOutOfStockException
from app.orders.models import Order, OrderItem
from app.cart.models import Cart
from app.products.models import Product
from datetime import datetime,timezone

#Function to empty the cart and make oders for that cart items
def perform_checkout(db: Session, user_id: int):
    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()

    if not cart_items:
        return None 

    total_amount = 0
    order_items = []

    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product or product.stock < item.quantity:
            raise ItemOutOfStockException(product.name)
        
        product.stock -= item.quantity
        subtotal = product.price * item.quantity
        total_amount += subtotal

        order_items.append(OrderItem(
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_purchase=product.price
        ))

    new_order = Order(
        user_id=user_id,
        total_amount=total_amount,
        status="paid",
        created_at=datetime.now(timezone.utc),
        order_items=order_items
    )

    db.add(new_order)
    db.query(Cart).filter(Cart.user_id == user_id).delete()
    db.commit()
    db.refresh(new_order)
    return new_order