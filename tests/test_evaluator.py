
from app.utils.validator import deterministic_checks


def test_missing_quiz_fails():
    lesson = "# Intro\n\n" + ("This is a simple lesson. " * 30)

    failures = deterministic_checks(lesson)

    assert "R10" in failures


def test_missing_example_fails():
    lesson = "# Summary\n\n" + ("A topic explained clearly. " * 30)

    failures = deterministic_checks(lesson)

    assert "R7" in failures


def test_five_numbered_questions_with_unicode_heading_pass():
    lesson = """
# Introduction to RAG

This is a beginner lesson about retrieval augmented generation.
RAG retrieves useful information before generating an answer.
For example, a system can search school notes.

## 7. Recap

RAG retrieves information and generates an answer.

## 8. Knowledge‑Check Questions

1. **What does RAG mean?**
   Answer: Retrieval-Augmented Generation.

2. **Why is RAG useful?**
   Answer: It retrieves relevant information.

3. **Name the three main components of RAG.**
   Answer: Encoder, Retriever, Generator.

4. **What does a retriever do?**
   Answer: It finds relevant documents.

5. **What is hallucination?**
   Answer: Generating incorrect or unsupported information.
"""

    failures = deterministic_checks(lesson)

    assert "R10" not in failures
