from langgraph.graph import StateGraph, END
from agents.router import router

builder = StateGraph(dict)

builder.add_node("router", router)

builder.set_entry_point("router")
builder.add_edge("router", END)

agent_graph = builder.compile()
