from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ChatBase(BaseModel):
    content: str
    max_tokens: Optional[int] = 150

class ChatCreate(ChatBase):
    pass

class ChatResponse(BaseModel):
    id: int
    content: str
    response: str
    created_at: datetime
    tokens_used: Optional[int]

    class Config:
        from_attributes = True
