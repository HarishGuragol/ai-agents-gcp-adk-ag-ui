# api/app.py

from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
from agents.orchestrator import orchestrate
import json

app = FastAPI()

@app.get("/")
def index():
    with open("static/index.html") as f:
        return HTMLResponse(f.read())

@app.get("/chat")
async def chat(query: str):
    async def event_stream():
        async for event in orchestrate(query):
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")

