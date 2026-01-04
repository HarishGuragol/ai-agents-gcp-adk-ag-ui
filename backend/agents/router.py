# agents/router.py

# agents/router.py
# agents/router.py

def router(state):
    query = state["query"]
    return {
        **state,
        "agent_type": "ops"
    }

