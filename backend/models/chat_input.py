from pydantic import BaseModel

class ChatInput(BaseModel):
    message: str
    mode: str # chat or agent