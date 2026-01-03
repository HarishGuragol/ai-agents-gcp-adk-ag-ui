from fastapi.responses import HTMLResponse
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
import uuid

from agents.orchestrator import orchestrate

from ag_ui.core.events import (
    RunStartedEvent,
    RunFinishedEvent,
    ThinkingStartEvent,
    ThinkingEndEvent,
    TextMessageStartEvent,
    TextMessageContentEvent,
    TextMessageEndEvent,
)

app = FastAPI()


async def agui_stream(query: str):
    thread_id = str(uuid.uuid4())
    run_id = str(uuid.uuid4())
    message_id = str(uuid.uuid4())

    # RUN STARTED
    yield RunStartedEvent(
        thread_id=thread_id,
        run_id=run_id,
    ).model_dump_json() + "\n\n"

    await asyncio.sleep(0.1)

    # THINKING START
    yield ThinkingStartEvent(
        title="Routing request"
    ).model_dump_json() + "\n\n"

    # EXECUTE AGENT
    result = orchestrate(query)

    # THINKING END
    yield ThinkingEndEvent().model_dump_json() + "\n\n"

    # MESSAGE START
    yield TextMessageStartEvent(
        message_id=message_id,
        role="assistant",
    ).model_dump_json() + "\n\n"

    # MESSAGE CONTENT (streamed)
    for word in result.split():
        yield TextMessageContentEvent(
            message_id=message_id,
            delta=word + " ",
        ).model_dump_json() + "\n\n"
        await asyncio.sleep(0.05)

    # MESSAGE END
    yield TextMessageEndEvent(
        message_id=message_id
    ).model_dump_json() + "\n\n"

    # RUN FINISHED
    yield RunFinishedEvent(
        thread_id=thread_id,
        run_id=run_id,
    ).model_dump_json() + "\n\n"

@app.get("/", response_class=HTMLResponse)
def ui():
    return Path("ui/index.html").read_text()

from fastapi import Request
from fastapi.responses import StreamingResponse

@app.get("/chat")
async def chat(request: Request, query: str):

    async def event_generator():
        # 🔥 1. Immediate flush so proxy keeps connection
        yield ": connected\n\n"

        async def heartbeat():
            while True:
                await asyncio.sleep(2)
                yield ": ping\n\n"

        hb = heartbeat()

        try:
            async for event in agui_stream(query):
                yield f"data: {event}\n\n"
        except Exception as e:
            yield f"data: {{\"type\":\"RUN_ERROR\",\"error\":\"{str(e)}\"}}\n\n"
        finally:
            hb.aclose()

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


