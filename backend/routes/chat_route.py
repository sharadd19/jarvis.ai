from fastapi import APIRouter
from backend.services.model_picker import model_picker
from backend.models.ChatInputModel import ChatInput

router = APIRouter()

@router.post("/")
async def chat(input: ChatInput):
    if input.mode == "Agent":
        return "Agent mode is not supported yet"
    else: 
        return await model_picker(input)