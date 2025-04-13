from pydantic import BaseModel

class ChatInput(BaseModel):
    message: str 
    mode: str = "Chat" # chat or agent
    model: str  = "gemini-2.0-flash" # gpt4o, etc