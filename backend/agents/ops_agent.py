from uuid import uuid4

def run_ops_agent(state: dict):
    query = state["query"]
    message_id = str(uuid4())

    yield {
        "type": "THINKING_START",
        "title": "Ops agent processing request"
    }

    yield {
        "type": "TEXT_MESSAGE_START",
        "message_id": message_id,
        "role": "assistant"
    }

    text = f"Cloud Run is a fully managed serverless platform on GCP. You asked: {query}"

    for token in text.split():
        yield {
            "type": "TEXT_MESSAGE_CONTENT",
            "message_id": message_id,
            "delta": token + " "
        }

    yield {
        "type": "TEXT_MESSAGE_END",
        "message_id": message_id
    }

    yield {
        "type": "THINKING_END"
    }
