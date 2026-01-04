from agents.graph import agent_graph
from agents.ops_agent import run_ops_agent

async def orchestrate(query: str):
    yield {"type": "RUN_STARTED"}

    state = {"query": query}
    result = agent_graph.invoke(state)

    if result["agent_type"] == "ops":
        for event in run_ops_agent(result):
            yield event

    yield {"type": "RUN_FINISHED"}
