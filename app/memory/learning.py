from app.memory.database import get_memory_guidance

def build_learning_context() -> str:
    """Turn recurring historical failure patterns into generation guidance."""
    return get_memory_guidance()
