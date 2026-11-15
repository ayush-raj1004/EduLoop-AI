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

Be technically accurate. Do not invent statistics, citations, product claims,
or facts. If a detail is uncertain, qualify it instead of presenting it as fact.
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
