from pydantic import BaseModel, Field
from typing import Optional, Any


class DishCreate(BaseModel):
    dish_code: str
    dish_name: str
    calorie_count: int
    price: float
    status: str = Field(default="AVAILABLE")

class DishUpdate(BaseModel):
    dish_code: str
    dish_name: str
    calorie_count: int
    price: float
    status: str 

class BaseResponse(BaseModel):
    status_code: int
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None
    timestamp: str
    path: str
