from typing import Any, TypedDict


class WorkflowState(TypedDict, total=False):
    topic: str
    lesson: str
    evaluation: dict[str, Any]
    feedback: str
    attempt: int
    max_retries: int
    passed: bool
    rejections: list[dict[str, Any]]
    memory_guidance: str
    status: str
    run_id: int
