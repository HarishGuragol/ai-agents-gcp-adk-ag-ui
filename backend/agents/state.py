from typing import TypedDict, Literal

class AgentState(TypedDict):
    query: str
    agent_type: Literal["ops", "research", "fallback"]
    response: str
