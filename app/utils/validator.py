
import re


def deterministic_checks(lesson: str) -> dict[str, str]:
    """Return hard failures that can be checked without an LLM."""
    failures = {}

    # Normalize Unicode hyphens and dashes.
    normalized_lines = [
        line.translate(str.maketrans({
            "\u2010": "-",
            "\u2011": "-",
            "\u2012": "-",
            "\u2013": "-",
            "\u2014": "-",
            "\u2212": "-",
        }))
        for line in lesson.splitlines()
    ]

    # Find the knowledge-check section by its heading.
    start_index = None

    for index, line in enumerate(normalized_lines):
        heading = line.strip().lower()

        if (
            heading.startswith("#")
            and "knowledge" in heading
            and "check" in heading
            and "question" in heading
        ):
            start_index = index + 1
            break

    question_count = 0

    if start_index is not None:
        section_lines = []

        for line in normalized_lines[start_index:]:
            if re.match(r"^\s*#{1,6}\s+", line):
                break
            section_lines.append(line)

        question_section = "\n".join(section_lines)

        numbered_questions = re.findall(
            r"(?m)^\s*\d+[\).]\s+\*\*.+?\*\*",
            question_section,
        )

        question_count = len(numbered_questions)

    if question_count < 5:
        failures["R10"] = (
            f"Found only {question_count} numbered knowledge-check questions; "
            "at least five numbered questions are required."
        )

    text = lesson.lower()

    if len(lesson.split()) < 350:
        failures["R9"] = (
            "Lesson is shorter than 350 words; it may not provide enough "
            "standalone teaching context."
        )

    if not any(term in text for term in ("recap", "summary", "key takeaways")):
        failures["R10"] = (
            failures.get("R10", "")
            + " A recap/summary section is missing."
        ).strip()

    if not any(term in text for term in ("example", "for example", "imagine")):
        failures["R7"] = "No clear practical example marker was found."

    if not any(term in text for term in ("retriev", "search", "find")) and "rag" in text:
        failures["R6"] = "No retrieval/search stage was detected."

    return failures
