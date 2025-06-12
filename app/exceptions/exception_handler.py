from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.logger import logger
from app.exceptions.exception import (
    DuplicateEmailException,
    UserNotFoundException,
    ProductNotFoundException,
    CartItemNotFoundException,
    EmptyCartException,
    ItemOutOfStockException,
    InvalidCredentialsException,
    OrderNotFoundException,
)


def exception_handlers(app):
    
    @app.exception_handler(DuplicateEmailException)
    async def duplicate_email_exception_handler(request: Request, exc: DuplicateEmailException):
        logger.warning(f"[{request.method} {request.url.path}] Duplicate email: {exc.email}")
        return JSONResponse(
            status_code=400,
            content={"error": True,
                "message": f"Email '{exc.email}' is already registered",
                "code": 400}
        )
    
    @app.exception_handler(InvalidCredentialsException)
    async def invalid_credentials_exception_handler(request: Request, exc: InvalidCredentialsException):
        logger.warning(f"[{request.method} {request.url.path}] Invalid credentials")
        return JSONResponse(
            status_code=401,
            content={ "error": True,
                "message": exc.message,
                "code": 401}
        )

    @app.exception_handler(UserNotFoundException)
    async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
        logger.warning(f"[{request.method} {request.url.path}] User not found: {exc.message}")
        return JSONResponse(
            status_code=400,
            content={"error": True,
                "message": exc.message,
                "code": 400}
        )
    
    @app.exception_handler(ProductNotFoundException)
    async def product_not_found_exception_handler(request: Request, exc: ProductNotFoundException):
        logger.warning(f"[{request.method} {request.url.path}] Product not found: {exc.message}")
        return JSONResponse(
            status_code=400,
            content={"error": True,
                "message": exc.message,
                "code": 400}
        )

    @app.exception_handler(ItemOutOfStockException)
    async def item_out_of_stock_exception_handler(request: Request, exc: ItemOutOfStockException):
        logger.warning(f"[{request.method} {request.url.path}] Out of stock: {exc.item_name}")
        return JSONResponse(
            status_code=400,
            content={"error": True,
                "message": f"The item '{exc.item_name}' is out of stock.",
                "code": 400}
        )

    
    @app.exception_handler(CartItemNotFoundException)
    async def cart_item_not_found_handler(request: Request, exc: CartItemNotFoundException):
        logger.warning(f"[{request.method} {request.url.path}] Cart item not found: Product ID {exc.item_id}")
        return JSONResponse(
            status_code=404,
            content={ "error": True,
                "message": f"Cart item with product id {exc.item_id} not found.",
                "code": 404}
        )

    @app.exception_handler(EmptyCartException)
    async def empty_cart_exception_handler(request: Request, exc: EmptyCartException):
        logger.warning(f"[{request.method} {request.url.path}] Empty cart: {exc.message}")
        return JSONResponse(
        status_code=400,
        content={"error": True,
                "message": exc.message,
                "code": 400}
    )

    @app.exception_handler(OrderNotFoundException)
    async def order_not_found_handler(request: Request, exc: OrderNotFoundException):
        logger.warning(f"[{request.method} {request.url.path}] Order not found: {exc.message}")
        return JSONResponse(
        status_code=404,
        content={"error": True,
                "message": exc.message,
                "code": 404}
    )



