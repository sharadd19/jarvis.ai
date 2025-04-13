from fastapi import APIRouter
from fastapi.responses import JSONResponse
from backend.models.AgentInputModel import AgentInput
from backend.services.agent import agent_mode

router = APIRouter()

@router.post("/")
async def agent(input: AgentInput):
    try: 
        result = await agent_mode(input)
        return result
    except Exception as e:  
        return JSONResponse(status_code=500, content={"error": str(e)})
        