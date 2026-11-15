
from app.graph.nodes import route_after_evaluation


def test_pass_routes_to_save():
    state = {"passed": True, "attempt": 1, "max_retries": 2}
    assert route_after_evaluation(state) == "save"


def test_failure_with_retry_remaining_routes_to_retry():
    state = {"passed": False, "attempt": 1, "max_retries": 2}
    assert route_after_evaluation(state) == "retry"


def test_failure_at_last_attempt_routes_to_save():
    state = {"passed": False, "attempt": 3, "max_retries": 2}
    assert route_after_evaluation(state) == "save"


def test_historical_memory_is_loaded_before_first_generation(monkeypatch):
    import app.graph.workflow as workflow_module

    captured = {}
    expected_guidance = "Historical guidance: explain examples clearly."

    class FakeApp:
        def invoke(self, state):
            captured["state"] = state
            return state

    monkeypatch.setattr(
        workflow_module,
        "build_learning_context",
        lambda: expected_guidance,
    )

    monkeypatch.setattr(
        workflow_module,
        "build_workflow",
        lambda: FakeApp(),
    )

    workflow_module.run_lesson_workflow("Introduction to RAG")

    assert captured["state"]["attempt"] == 1
    assert captured["state"]["memory_guidance"] == expected_guidance
