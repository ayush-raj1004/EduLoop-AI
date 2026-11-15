from app.agents.generator import generate_lesson
from app.agents.evaluator import evaluate_lesson
from app.graph.state import WorkflowState
from app.memory.database import save_run
from app.memory.learning import build_learning_context


def generate_node(state: WorkflowState) -> dict:
    lesson = generate_lesson(
        topic=state["topic"],
        feedback=state.get("feedback", ""),
        memory_guidance=state.get("memory_guidance", ""),
    )
    return {"lesson": lesson}


def evaluate_node(state: WorkflowState) -> dict:
    result = evaluate_lesson(state["topic"], state["lesson"])
    failures = result.failures
    feedback = "\n".join(
        f"{item.check_id} – {item.name}: {item.reason} "
        f"Suggested fix: {item.suggested_fix}"
        for item in failures
    )
    rejections = list(state.get("rejections", []))
    if not result.passed:
        rejections.append({
            "attempt": state["attempt"],
            "failures": [item.model_dump() for item in failures],
            "feedback": feedback or result.overall_feedback,
        })
    return {
        "evaluation": result.model_dump(),
        "passed": result.passed,
        "feedback": feedback,
        "rejections": rejections,
    }


def route_after_evaluation(state: WorkflowState) -> str:
    if state.get("passed"):
        return "save"
    if state["attempt"] <= state["max_retries"]:
        return "retry"
    return "save"


def retry_node(state: WorkflowState) -> dict:
    return {
        "attempt": state["attempt"] + 1,
        "memory_guidance": build_learning_context(),
    }


def save_node(state: WorkflowState) -> dict:
    status = "APPROVED" if state.get("passed") else "REJECTED_FOR_HUMAN_REVIEW"
    run_id = save_run(
        topic=state["topic"],
        status=status,
        attempts=state["attempt"],
        lesson=state.get("lesson", ""),
        evaluation=state.get("evaluation", {}),
        rejections=state.get("rejections", []),
    )
    return {"status": status, "run_id": run_id}
