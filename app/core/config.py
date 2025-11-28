from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://tele-mess:3344Frzaq0607@db:5432/mess"
    
    SECRET_KEY: str = "f8134dea6e71a1884d799b4a453ad93cbb7736358eceda96da85714c038d8635"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    WS_HOST: str = "0.0.0.0"
    WS_PORT: int = 8000

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

settings = Settings()
print(f"DATABASE_URL: {settings.DATABASE_URL}")