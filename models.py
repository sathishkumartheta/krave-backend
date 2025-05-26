from pydantic import BaseModel
from typing import Optional

class FoodRequest(BaseModel):
    description: Optional[str] = None
    image_url: Optional[str] = None  # or you can use base64 if preferred
