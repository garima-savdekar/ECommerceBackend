class DuplicateEmailException(Exception):
    def __init__(self, email: str):
        self.email = email
        
class UserNotFoundException(Exception):
    def __init__(self, message: str = "User Not Found"):
        self.message = message
    
class ProductNotFoundException(Exception):
    def __init__(self, message: str = "Product Not Found"):
        self.message = message

class InvalidCredentialsException(Exception):
    def __init__(self, message: str = "Invalid email or password"):
        self.message = message

class CartItemNotFoundException(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id
    
class ItemOutOfStockException(Exception):
    def __init__(self, item_name: str):
        self.item_name = item_name

class EmptyCartException(Exception):
    def __init__(self):
        self.message = "Cart is empty"

class OrderNotFoundException(Exception):
    def __init__(self, order_id=None):
        self.message = "Order not found"
        if order_id:
            self.message += f" with id {order_id}"