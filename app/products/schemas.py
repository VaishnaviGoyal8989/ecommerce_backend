from pydantic import BaseModel, Field
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: str
    price: float=Field(..., gt=0, description="Price should be positive")
    stock: int=Field(..., ge=0, description="enter valid stock")
    category: str
    image_url: str

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0, description="Price should be positive")
    stock: Optional[int] = Field(None, ge=0, description="enter valid stock")
    category: Optional[str] = None
    image_url: Optional[str] = None

class ProductOut(ProductBase):
    id: int
    model_config = {
        "from_attributes": True
    }
