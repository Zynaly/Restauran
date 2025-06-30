from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.OrderOut)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    # Verify all items exist and are available
    items = db.query(models.MenuItem).filter(
        models.MenuItem.id.in_(order.item_ids),
        models.MenuItem.is_available == True
    ).all()
    
    if len(items) != len(order.item_ids):
        raise HTTPException(status_code=400, detail="Some items are not available or don't exist")
    
    db_order = models.Order(customer_name=order.customer_name)
    db_order.items = items
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/", response_model=List[schemas.OrderOut])
def get_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()

@router.get("/{order_id}", response_model=schemas.OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order