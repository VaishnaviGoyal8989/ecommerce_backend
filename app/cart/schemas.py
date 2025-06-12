from pydantic import BaseModel, Field

class CartItemBase(BaseModel):
    product_id: int
    quantity: int=Field(..., gt=0, description="enter valid quantity")

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    quantity: int=Field(..., gt=0, description="enter valid quantity")

class CartItemOut(CartItemBase):
    id: int
    
    model_config = {
        "from_attributes": True
    }
