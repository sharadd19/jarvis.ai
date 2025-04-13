from typing import Optional
from pydantic import BaseModel

class AgentInput(BaseModel):
    message: str 
    mode: str = "Agent" # chat or agent
    model: str  = "gemini-2.0-flash" # gpt4o, etc
    tool: Optional[str] =  None # Optional MCP server URL
