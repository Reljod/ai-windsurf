from fastapi import FastAPI
from app.api import chat
from app.db.database import engine
from app.models import chat as chat_model

# Create database tables
chat_model.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ChatGPT API",
    description="A REST API for interacting with ChatGPT",
    version="1.0.0"
)

# Include routers
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
