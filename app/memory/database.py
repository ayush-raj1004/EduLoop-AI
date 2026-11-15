
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from app.config import settings


def get_connection():
    Path(settings.DATABASE_PATH).parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    conn = sqlite3.connect(settings.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS runs (
                run_id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                status TEXT NOT NULL,
                attempts INTEGER NOT NULL,
                final_lesson TEXT,
                evaluation_json TEXT,
                created_at TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS rejection_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id INTEGER NOT NULL,
                attempt INTEGER NOT NULL,
                failures_json TEXT NOT NULL,
                feedback TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(run_id) REFERENCES runs(run_id)
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS failure_patterns (
                pattern TEXT PRIMARY KEY,
                occurrences INTEGER NOT NULL DEFAULT 1,
                updated_at TEXT NOT NULL
            )
        """)


def save_run(topic, status, attempts, lesson, evaluation, rejections):
    now = datetime.now(timezone.utc).isoformat()

    with get_connection() as conn:
        cursor = conn.execute(
            """INSERT INTO runs
            (topic, status, attempts, final_lesson,
             evaluation_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (
                topic,
                status,
                attempts,
                lesson,
                json.dumps(evaluation, ensure_ascii=False),
                now,
            ),
        )

        run_id = cursor.lastrowid

        for entry in rejections:
            conn.execute(
                """INSERT INTO rejection_logs
                (run_id, attempt, failures_json, feedback, created_at)
                VALUES (?, ?, ?, ?, ?)""",
                (
                    run_id,
                    entry["attempt"],
                    json.dumps(
                        entry["failures"],
                        ensure_ascii=False,
                    ),
                    entry["feedback"],
                    now,
                ),
            )

            for failure in entry["failures"]:
                check_id = failure.get("check_id", "unknown")
                name = failure.get("name", "Unknown requirement")
                reason = failure.get("reason", "Reason not provided")
                suggested_fix = failure.get(
                    "suggested_fix",
                    "Review this requirement carefully.",
                )

                # Store the actual reason and suggested correction.
                pattern = (
                    f"{check_id} - {name}: {reason} "
                    f"Suggested fix: {suggested_fix}"
                )

                conn.execute("""
                    INSERT INTO failure_patterns
                    (pattern, occurrences, updated_at)
                    VALUES (?, 1, ?)
                    ON CONFLICT(pattern) DO UPDATE SET
                    occurrences = occurrences + 1,
                    updated_at = excluded.updated_at
                """, (pattern, now))

        return run_id


def get_memory_guidance(limit=5):
    initialize_database()

    with get_connection() as conn:
        rows = conn.execute("""
            SELECT pattern, occurrences
            FROM failure_patterns
            ORDER BY occurrences DESC, updated_at DESC
            LIMIT ?
        """, (limit,)).fetchall()

    if not rows:
        return ""

    return "\n".join(
        f"- Previous issue: {row['pattern']} "
        f"(observed {row['occurrences']} time(s)). "
        "Check and prevent this issue in the new lesson."
        for row in rows
    )


def get_recent_runs(limit=20):
    initialize_database()

    with get_connection() as conn:
        rows = conn.execute("""
            SELECT run_id, topic, status, attempts, created_at
            FROM runs
            ORDER BY run_id DESC
            LIMIT ?
        """, (limit,)).fetchall()

    return [dict(row) for row in rows]


initialize_database()
