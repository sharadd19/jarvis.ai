from fastapi import APIRouter
import os
from fastapi.responses import StreamingResponse
import google.generativeai as genai

from models.chat_input import ChatInput

router = APIRouter()

# Load API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create model instance
model = genai.GenerativeModel("gemini-2.0-flash")  # or "gemini-pro", "gemini-1.5-pro" as needed

@router.post("/")
async def chat(input: ChatInput):
    if input.mode == "Agent":
        return "Agent mode activated"
    else:
        response = await model.generate_content_async(
            [input.message],
            stream=True)
        
        async def stream_chunks():
            async for chunk in response:
                if chunk.text:
                    yield chunk.text
        return StreamingResponse(stream_chunks())
