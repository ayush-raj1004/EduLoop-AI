from app.agents.generator import get_llm
from app.config import settings
from app.prompts.evaluator_prompt import EVALUATOR_SYSTEM_PROMPT
from app.schemas.evaluation import EvaluationResult
from app.utils.validator import deterministic_checks


def evaluate_lesson(topic: str, lesson: str) -> EvaluationResult:
    llm = get_llm(settings.EVALUATION_TEMPERATURE)
    structured_llm = llm.with_structured_output(EvaluationResult)
    result = structured_llm.invoke([
        ("system", EVALUATOR_SYSTEM_PROMPT),
        ("human", f"Topic: {topic}\n\nEvaluate this lesson:\n\n{lesson}"),
    ])

    # Deterministic checks can turn an LLM PASS into FAIL, never the reverse.
    hard_failures = deterministic_checks(lesson)
    by_id = {check.check_id: check for check in result.checks}
    for check_id, reason in hard_failures.items():
        if check_id in by_id:
            by_id[check_id].status = "FAIL"
            by_id[check_id].reason = (
                f"Deterministic validation failed: {reason}. "
                + by_id[check_id].reason
            )
            by_id[check_id].suggested_fix = (
                "Add the missing required content and regenerate."
            )

    result.checks = [by_id.get(f"R{i}") for i in range(1, 11)]
    if any(item is None for item in result.checks):
        raise ValueError("Evaluator did not return exactly R1-R10.")
    return result
