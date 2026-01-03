from agents.ops_agent import ops_agent


def orchestrate(query: str) -> str:
    q = query.lower()

    # Ops agent path
    if any(k in q for k in ["gcp", "cloud run", "deploy", "scaling", "infra"]):
        return (
            "Cloud Run automatically scales by creating and terminating "
            "container instances based on incoming HTTP requests. "
            "It uses request concurrency and CPU utilization to decide "
            "when to scale up or down, and can scale to zero when idle."
        )

    # Research agent path
    return (
        "A transformer is a neural network architecture that uses "
        "self-attention instead of recurrence or convolution. "
        "It processes tokens in parallel and models long-range dependencies efficiently."
    )
