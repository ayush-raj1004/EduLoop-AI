from typing import Literal
from pydantic import BaseModel, Field


class RubricCheck(BaseModel):
    check_id: str
    name: str
    status: Literal["PASS", "FAIL"]
    reason: str
    suggested_fix: str = ""


class EvaluationResult(BaseModel):
    checks: list[RubricCheck] = Field(min_length=10, max_length=10)
    overall_feedback: str

    @property
    def passed(self) -> bool:
        required = {f"R{i}" for i in range(1, 11)}
        actual = {item.check_id for item in self.checks}
        return actual == required and all(item.status == "PASS" for item in self.checks)

    @property
    def failures(self) -> list[RubricCheck]:
        return [item for item in self.checks if item.status == "FAIL"]
