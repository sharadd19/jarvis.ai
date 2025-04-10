from pathlib import Path
from dotenv import load_dotenv
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)
from fastapi import FastAPI
from routes import chat, stream, agent


app = FastAPI()
app.include_router(chat.router, prefix="/chat")
app.include_router(stream.router, prefix="/stream")
app.include_router(agent.router, prefix="/agent")