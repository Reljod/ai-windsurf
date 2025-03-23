import os

from fastapi import FastAPI, HTTPException
from httpx import Client
from openai import OpenAI
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="ChatGPT API", description="A REST API for interacting with ChatGPT")

# Configure OpenAI
api_key = os.getenv("OPENAI_API_KEY")
httpx_client = Client()
client = OpenAI(api_key=api_key, http_client=httpx_client)

class Message(BaseModel):
    content: str
    max_tokens: Optional[int] = 150

class Request(BaseModel):
    message: Message
    model: str

class ChatResponse(BaseModel):
    response: str

@app.post("/message", response_model=ChatResponse)
async def get_chat_response(request: Request):
    try:
        # Create chat completion
        response = client.chat.completions.create(
            model=request.model,
            messages=[
                {"role": "user", "content": request.message.content}
            ],
            max_tokens=request.message.max_tokens
        )

        # Extract the response text
        response_text = response.choices[0].message.content

        return ChatResponse(response=response_text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
