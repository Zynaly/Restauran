from pydantic import BaseModel
from typing import List
from datetime import datetime

class MenuItemBase(BaseModel):
    name: str
    price: float
    is_available: bool

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemOut(MenuItemBase):
    id: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Margherita Pizza",
                "price": 12.99,
                "is_available": True
            }
        }

class OrderCreate(BaseModel):
    customer_name: str
    item_ids: List[int]

class OrderOut(BaseModel):
    id: int
    customer_name: str
    created_at: datetime
    items: List[MenuItemOut]
    total_price: float  

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "customer_name": "John Doe",
                "created_at": "2025-06-30T12:00:00Z",
                "items": [
                    {
                        "id": 1,
                        "name": "Margherita Pizza",
                        "price": 12.99,
                        "is_available": True
                    }
                ],
                "total_price": 12.99
            }
        }