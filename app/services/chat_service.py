import openai
from sqlalchemy.orm import Session
from app.models.chat import Chat
from app.schemas.chat import ChatCreate
from app.core.config import settings

class ChatService:
    def __init__(self, openai_client):
        self.client = openai_client

    async def create_chat(self, db: Session, chat: ChatCreate) -> Chat:
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": chat.content}],
            max_tokens=chat.max_tokens
        )

        ai_response = response.choices[0].message.content
        tokens_used = response.usage.total_tokens

        db_chat = Chat(
            content=chat.content,
            response=ai_response,
            tokens_used=tokens_used
        )

        db.add(db_chat)
        db.commit()
        db.refresh(db_chat)

        return db_chat
