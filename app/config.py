from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    SERPER_API_KEY: str
    PORT: int = 4000

    class Config:
        env_file = ".env"

settings = Settings()
