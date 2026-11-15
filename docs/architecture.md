# Architecture

1. Input validation checks that a topic is present.
2. Generator agent creates a standalone beginner lesson.
3. Evaluator agent independently judges the lesson against ten binary checks.
4. Deterministic validators can downgrade a model PASS to FAIL when required
   structural content is missing.
5. LangGraph routes a passing lesson to persistence, or a failed lesson to
   rejection logging and a retry when attempts remain.
6. SQLite stores run outcomes, evaluation records, rejection details and
   recurring failed rubric IDs.
7. Memory guidance from recurring failures is included in future generation
   prompts. The rubric itself remains fixed.

Maximum attempts = 1 initial generation + 2 retries.
