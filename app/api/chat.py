import os

from fastapi import APIRouter, Depends, HTTPException
from httpx import Client
from openai import OpenAI
from sqlalchemy.orm import Session

from app.schemas.chat import ChatCreate, ChatResponse
from app.services.chat_service import ChatService
from app.db.database import get_db
from app.core.config import settings

httpx_client = Client()
client = OpenAI(api_key=settings.OPENAI_API_KEY, http_client=httpx_client)

router = APIRouter()
chat_service = ChatService(openai_client=client)

@router.post("/chat", response_model=ChatResponse)
async def create_chat(
    chat: ChatCreate,
    db: Session = Depends(get_db)
):
    try:
        return await chat_service.create_chat(db, chat)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
