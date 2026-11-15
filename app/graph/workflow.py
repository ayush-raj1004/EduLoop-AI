
from langgraph.graph import StateGraph, START, END

from app.config import settings
from app.graph.state import WorkflowState
from app.graph.nodes import (
    generate_node,
    evaluate_node,
    retry_node,
    save_node,
    route_after_evaluation,
)
from app.memory.learning import build_learning_context


def build_workflow():
    graph = StateGraph(WorkflowState)

    graph.add_node("generate", generate_node)
    graph.add_node("evaluate", evaluate_node)
    graph.add_node("retry", retry_node)
    graph.add_node("save", save_node)

    graph.add_edge(START, "generate")
    graph.add_edge("generate", "evaluate")

    graph.add_conditional_edges(
        "evaluate",
        route_after_evaluation,
        {
            "retry": "retry",
            "save": "save",
        },
    )

    graph.add_edge("retry", "generate")
    graph.add_edge("save", END)

    return graph.compile()


def run_lesson_workflow(topic: str, max_retries: int | None = None):
    topic = topic.strip()

    if not topic:
        raise ValueError("Topic cannot be empty.")

    retries = (
        settings.MAX_RETRIES
        if max_retries is None
        else max_retries
    )

    if retries < 0 or retries > 2:
        raise ValueError("max_retries must be between 0 and 2.")

    app = build_workflow()

    # Load persistent memory before the first generation attempt.
    memory_guidance = build_learning_context()

    initial_state: WorkflowState = {
        "topic": topic,
        "attempt": 1,
        "max_retries": retries,
        "feedback": "",
        "rejections": [],
        "memory_guidance": memory_guidance,
        "passed": False,
    }

    return app.invoke(initial_state)
