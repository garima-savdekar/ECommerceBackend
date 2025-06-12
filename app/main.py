from fastapi import FastAPI
from app.auth import routes as auth_routes
from app.core.database import Base, engine
from app.exceptions.exception_handler import exception_handlers
from app.products.routes import admin_routes,public_routes
from app.cart import routes as cart_routes
from app.checkout import routes as checkout_routes
from app.orders import routes as order_routes

app = FastAPI()

exception_handlers(app)

Base.metadata.create_all(bind=engine)

app.include_router(auth_routes.router)

app.include_router(admin_routes.router)

app.include_router(public_routes.router)

app.include_router(cart_routes.router)

app.include_router(checkout_routes.router)

app.include_router(order_routes.router)
