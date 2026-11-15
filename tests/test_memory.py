
import sqlite3


def test_database_schema_can_be_created(tmp_path, monkeypatch):
    from app import config
    from app.memory import database

    db_path = tmp_path / "test.db"
    monkeypatch.setattr(
        config.settings,
        "DATABASE_PATH",
        str(db_path),
    )

    database.initialize_database()

    conn = sqlite3.connect(db_path)
    tables = {
        row[0]
        for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
    }
    conn.close()

    assert {
        "runs",
        "rejection_logs",
        "failure_patterns",
    }.issubset(tables)


def test_memory_stores_and_retrieves_detailed_failure(tmp_path, monkeypatch):
    from app import config
    from app.memory import database

    db_path = tmp_path / "memory_test.db"

    monkeypatch.setattr(
        config.settings,
        "DATABASE_PATH",
        str(db_path),
    )

    database.initialize_database()

    failure = {
        "check_id": "R10",
        "name": "Learning assessment",
        "status": "FAIL",
        "reason": "The lesson must contain at least five questions.",
        "suggested_fix": "Add five numbered questions with answers.",
    }

    rejection = {
        "attempt": 1,
        "failures": [failure],
        "feedback": "Please improve the knowledge-check section.",
    }

    # Save the same failure twice to verify occurrence counting.
    for _ in range(2):
        database.save_run(
            topic="Introduction to RAG",
            status="REJECTED_FOR_HUMAN_REVIEW",
            attempts=1,
            lesson="Test lesson",
            evaluation={},
            rejections=[rejection],
        )

    guidance = database.get_memory_guidance()

    assert "R10" in guidance
    assert "Learning assessment" in guidance
    assert "at least five questions" in guidance
    assert "Add five numbered questions with answers" in guidance
    assert "2 time(s)" in guidance
