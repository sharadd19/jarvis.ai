from pathlib import Path
from dotenv import load_dotenv
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)
from fastapi import FastAPI
from backend.routes import agent_route
from backend.routes import chat_route


app = FastAPI()
app.include_router(chat_route.router, prefix="/chat")
app.include_router(agent_route.router, prefix="/agent")