from fastapi.responses import StreamingResponse
from services.stream_utils import stream_error
from services.LLMs import gemini
from models.ChatInputModel import ChatInput

model_registry = {
    "gemini-2.0-flash": gemini.stream,
    "gpt4o": None,  # Placeholder for GPT-4o
}
async def model_picker(input: ChatInput):
    handler = model_registry.get(input.model)
    if not handler: 
        return StreamingResponse(stream_error(f"Model {input.model} not supported"))
    return await handler(input.message)
    

