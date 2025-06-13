from typing import List, Optional
from fastapi import APIRouter,Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.exceptions.exception import ProductNotFoundException
from app.products import schemas,crud
from app.products.schemas import ProductOut
from app.core.database import get_db
from app.auth.dependencies import get_current_user
from app.core.logger import logger

router=APIRouter(prefix="/products",tags=["Public Products"])


valid_sorting_fields = {"id", "price", "name"}

@router.get("",response_model=list[ProductOut])
def list_products(
    category: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    sort_by: Optional[str] =Query("id"),
    page: int = Query(1,ge=1),
    page_size: int = Query(10,ge=1,le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if sort_by not in valid_sorting_fields:
        logger.warning("Sort field is not valid")
        raise HTTPException(status_code=400, detail=f"Invalid sort field: {sort_by}")
    
    logger.info(f"User {current_user.id} listing products "
                f"with filters | category={category}, min_price={min_price}, max_price={max_price}, sort_by={sort_by}, page={page}, page_size={page_size}")
    return crud.products_listing(db, category, min_price, max_price, sort_by, page, page_size)


@router.get("/search", response_model=List[schemas.ProductOut])
def search_products(
    keyword: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    logger.info(f"User {current_user.id} searching products with keyword: {keyword}")
    return crud.search_products(db, keyword)

@router.get("/{product_id}", response_model=schemas.ProductOut)
def product_detail(product_id: int, db: Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    logger.info(f"User {current_user.id} viewing product ID: {product_id}")
    product = crud.get_product_by_id(db, product_id)
    if not product:
        logger.warning(f"Product ID {product_id} not found requested by user {current_user.id}")
        raise ProductNotFoundException()
    return product