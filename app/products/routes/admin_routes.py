from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.exceptions.exception import ProductNotFoundException
from app.products.schemas import ProductCreate, ProductUpdate, ProductOut
from app.products import crud
from app.auth.dependencies import require_admin
from app.core.logger import logger

router = APIRouter(prefix="/admin/products", tags=["Admin Products"])

@router.post("", response_model=ProductOut)
def create(product: ProductCreate, db: Session = Depends(get_db), current_user: dict = Depends(require_admin)):
    logger.info(f"Admin {current_user.id} creating product: {product.name}")
    return crud.create_product(db,product,current_user.id)


@router.get("", response_model=list[ProductOut])
def get_all_products(skip:int=0,limit:int=10,db: Session = Depends(get_db), current_user: dict = Depends(require_admin)):
    logger.info(f"Admin {current_user.id} retrieving all products (skip={skip}, limit={limit})")
    return crud.get_all_products(db,current_user.id,skip,limit)
    

@router.get("/{product_id}", response_model=ProductOut)
def get_product_by_id(product_id: int, db: Session = Depends(get_db), current_user: dict = Depends(require_admin)):
    logger.info(f"Admin {current_user.id} fetching product ID: {product_id}")
    product=crud.get_product_by_id(db,product_id,current_user.id)
  
    if not product:
        logger.warning(f"Product ID {product_id} not found for admin {current_user.id}")
        raise ProductNotFoundException()
    
    return product

@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, updated: ProductUpdate, db: Session = Depends(get_db),current_user: dict = Depends(require_admin)):
    logger.info(f"Admin {current_user.id} updating product ID: {product_id}")
    updated=crud.update_product(db,product_id, current_user.id, updated)
  
    if not updated:
        logger.warning(f"Update failed - Product ID {product_id} not found for admin {current_user.id}")
        raise ProductNotFoundException()
    
    return updated

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db),current_user: dict = Depends(require_admin)):
    logger.info(f"Admin {current_user.id} deleting product ID: {product_id}")
    deleted=crud.delete_product(db,product_id, current_user.id)
   
    if not deleted:
        logger.warning(f"Delete failed - Product ID {product_id} not found for admin {current_user.id}")
        raise ProductNotFoundException()
    logger.info(f"Admin {current_user.id} deleted product ID: {product_id}")
    return {"message": "Product deleted successfully"}





# raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail="Product  not found."