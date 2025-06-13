from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.products import models, schemas

#Add the new product in database
def create_product(db: Session, product: schemas.ProductCreate,admin_id:int):
    new_product = models.Product(**product.dict(),admin_id=admin_id)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

#Get all the products which are added by logged in admin
def get_all_products(db: Session, admin_id:int,skip: int = 0, limit: int = 10):
    return db.query(models.Product).filter(models.Product.admin_id == admin_id).offset(skip).limit(limit).all()

#Retreive product by particular given id
def get_product_by_id(db: Session, product_id: int, admin_id:int):
    return db.query(models.Product).filter(models.Product.id == product_id, models.Product.admin_id == admin_id).first()

#Update product which is added by logged in admin
def update_product(db: Session, product_id: int, admin_id: int, product_update: schemas.ProductUpdate):
    product = get_product_by_id(db, product_id, admin_id)
    if not product:
        return None
    for field, value in product_update.dict(exclude_unset=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product

#Delete product added by only logged in admin
def delete_product(db: Session, product_id: int, admin_id:int):
    product = get_product_by_id(db, product_id, admin_id)
    if not product:
        return False
    db.delete(product)
    db.commit()
    return True

#Get all products including filters
def products_listing(db: Session, category:str=None, min_price:float=None, max_price:float=None, sort_by:str="id", page:int=1, page_size:int=10):
    query = db.query(models.Product)

    if category:
        query = query.filter(models.Product.category == category)
    if min_price is not None:
        query = query.filter(models.Product.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Product.price <= max_price)

    if sort_by in ["price", "name", "id"]:
        query = query.order_by(getattr(models.Product, sort_by))

    return query.offset((page-1)*page_size).limit(page_size).all()

#Search product by keyword matches in name,description, category
def search_products(db: Session, keyword: str):
    return db.query(models.Product).filter(
        or_(
            models.Product.name.ilike(f"%{keyword}%"),
            models.Product.description.ilike(f"%{keyword}%"),
            models.Product.category.ilike(f"%{keyword}%")
            )
    ).all()

#Get the product of particular given id
def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()