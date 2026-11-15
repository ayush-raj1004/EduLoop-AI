import json
from pathlib import Path
from app.config import settings
from app.graph.workflow import run_lesson_workflow


def run(topic: str):
    result = run_lesson_workflow(topic)
    lesson = result.get("lesson", "")
    report = {
        "topic": topic,
        "status": result.get("status"),
        "attempts": result.get("attempt"),
        "passed": result.get("passed"),
        "evaluation": result.get("evaluation"),
        "rejections": result.get("rejections", []),
        "run_id": result.get("run_id"),
    }

    if lesson:
        lesson_path = Path(settings.LESSONS_DIR) / f"run_{result['run_id']}.md"
        lesson_path.write_text(lesson, encoding="utf-8")
        report["lesson_file"] = str(lesson_path)

    report_path = Path(settings.REPORTS_DIR) / f"run_{result['run_id']}.json"
    report_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return result
