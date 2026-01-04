from uuid import uuid4
from google import genai
import os

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

def run_ops_agent(state):
    query = state["query"]
    message_id = str(uuid4())

    yield {
        "type": "THINKING_START",
        "title": "Gemini processing request"
    }

    yield {
        "type": "TEXT_MESSAGE_START",
        "message_id": message_id,
        "role": "assistant"
    }

    stream = client.models.generate_content_stream(
        model="gemini-2.5-flash",   # ✅ WORKS on v1beta
        contents=query,
    )

    for chunk in stream:
        if chunk.text:
            yield {
                "type": "TEXT_MESSAGE_CONTENT",
                "message_id": message_id,
                "delta": chunk.text
            }

    yield {
        "type": "TEXT_MESSAGE_END",
        "message_id": message_id
    }

    yield {
        "type": "THINKING_END"
    }
