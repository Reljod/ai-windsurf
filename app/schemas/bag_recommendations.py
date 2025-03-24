from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime

class BagRecommendationResponse(BaseModel):
    id: int
    recommendations: str
    analyzed_products: int
    created_at: datetime
    tokens_used: int | None = None

    class Config:
        from_attributes = True
