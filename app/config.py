from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    GENERATION_TEMPERATURE: float = 0.4
    EVALUATION_TEMPERATURE: float = 0.0
    MAX_RETRIES: int = 2
    DATABASE_PATH: str = str(BASE_DIR / "outputs" / "eduloop.db")
    LESSONS_DIR: str = str(BASE_DIR / "outputs" / "lessons")
    REPORTS_DIR: str = str(BASE_DIR / "outputs" / "reports")

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
Path(settings.LESSONS_DIR).mkdir(parents=True, exist_ok=True)
Path(settings.REPORTS_DIR).mkdir(parents=True, exist_ok=True)
Path(settings.DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)
