from langchain_groq import ChatGroq
from app.config import settings
from app.prompts.generator_prompt import (
    GENERATOR_SYSTEM_PROMPT, build_generator_prompt
)


def get_llm(temperature: float):
    if not settings.GROQ_API_KEY:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Add it to your .env file."
        )
    return ChatGroq(
        model=settings.GROQ_MODEL,
        api_key=settings.GROQ_API_KEY,
        temperature=temperature,
    )


def generate_lesson(topic: str, feedback: str = "",
                   memory_guidance: str = "") -> str:
    llm = get_llm(settings.GENERATION_TEMPERATURE)
    response = llm.invoke([
        ("system", GENERATOR_SYSTEM_PROMPT),
        ("human", build_generator_prompt(topic, feedback, memory_guidance)),
    ])
    content = response.content
    if not isinstance(content, str) or not content.strip():
        raise ValueError("The lesson generator returned empty content.")
    return content.strip()
