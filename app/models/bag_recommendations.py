from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from app.db.database import Base

class BagRecommendation(Base):
    __tablename__ = "bag_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    recommendations = Column(Text, nullable=False)
    analyzed_products = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    tokens_used = Column(Integer, nullable=True)
