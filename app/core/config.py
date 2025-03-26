from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SCORING_BASE_URL: str
    CORE_BANKING_USERNAME: str
    CORE_BANKING_PASSWORD: str
    CLIENT_NAME: str
    CLIENT_USERNAME: str
    CLIENT_PASSWORD: str
    RETRY_LIMIT: int

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
