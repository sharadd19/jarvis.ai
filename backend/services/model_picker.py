from fastapi.responses import StreamingResponse
from backend.services.stream_utils import stream_error
from backend.services.LLMs import gemini
from backend.models.ChatInputModel import ChatInput

MODEL_REGISTRY = {
    "gemini-2.0-flash": gemini.stream,
    "gpt4o": None,  # Placeholder for GPT-4o
}
async def model_picker(input: ChatInput):
    handler = MODEL_REGISTRY.get(input.model)
    if not handler: 
        return StreamingResponse(stream_error(f"Model {input.model} not supported"))
    return await handler(input.message)
    

