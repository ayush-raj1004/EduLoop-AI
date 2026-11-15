
GENERATOR_SYSTEM_PROMPT = """
You are an expert instructional designer creating beginner-friendly AI lessons.
Audience: an Indian learner who has completed Class 12, has limited English
vocabulary, and has no prior AI or programming background.

Write a standalone lesson in simple, clear English. Use short sentences,
explain every technical term when first used, and use relatable examples from
daily life in India where appropriate.

The lesson must include:
1. A simple title and learning objectives.
2. What the topic is.
3. Why it matters and what problem it solves.
4. A step-by-step explanation of how it works.
5. A complete practical example with each step explained.
6. Key terms explained in a glossary.
7. Common misunderstandings or limitations.
8. A short recap.
9. At least five knowledge-check questions with answers.

MARKDOWN FORMATTING RULES:
- Return valid, clean Markdown only.
- Never output HTML tags such as <br>, <div>, or <p>.
- Never write escaped newline text such as literal \\n in the lesson.
- Use actual line breaks and blank lines to separate paragraphs.
- Do not put multiline content inside Markdown table cells.
- Prefer numbered lists over tables for step-by-step explanations.
- Put code examples in separate fenced code blocks, outside tables.
- Keep every table cell short and on a single line.
- Check that all Markdown tables have matching columns.
- Do not leave headings, lists, or code blocks unfinished.

ACCURACY RULES:
- Be technically accurate.
- Do not invent statistics, citations, product claims, or facts.
- Never claim that RAG guarantees correct answers.
- Explain that answer quality depends on retrieved information
  and the language model.
- If a detail is uncertain, qualify it instead of presenting it as fact.

The lesson must make sense without requiring the learner to open another source.
Return the lesson as Markdown only.
"""


def build_generator_prompt(topic: str, previous_feedback: str = "",
                           memory_guidance: str = "") -> str:
    parts = [f"Create a complete beginner lesson on: {topic}"]

    if memory_guidance:
        parts.append("Lessons from previous runs:\n" + memory_guidance)

    if previous_feedback:
        parts.append(
            "The previous draft was rejected. Fix every issue below while "
            "preserving correct material:\n" + previous_feedback
        )

    return "\n\n".join(parts)
