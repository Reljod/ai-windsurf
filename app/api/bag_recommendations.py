import os
from fastapi import APIRouter, Depends, HTTPException
from httpx import Client
from openai import OpenAI
from sqlalchemy.orm import Session

from app.schemas.bag_recommendations import BagRecommendationResponse
from app.services.bag_recommendation_service import BagRecommendationService
from app.db.database import get_db
from app.core.config import settings

httpx_client = Client()
client = OpenAI(api_key=settings.OPENAI_API_KEY, http_client=httpx_client)

router = APIRouter()
bag_recommendation_service = BagRecommendationService(openai_client=client)

@router.post("/bag-recommendations", response_model=BagRecommendationResponse)
async def create_bag_recommendation(
    db: Session = Depends(get_db)
):
    """
    Generate AI-powered recommendations for bag improvements based on customer satisfaction data.
    """
    try:
        data_file_path = "scenarios/bag_satisfaction.json"
        return await bag_recommendation_service.get_bag_recommendations(db, data_file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
