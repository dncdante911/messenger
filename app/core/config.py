from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Конфигурация БД (остается как есть, загружается из .env)
    DB_HOST: str = Field(default="db")
    DB_PORT: int = Field(default=5432)
    DB_USER: str = Field(default="tele-mess")
    DB_PASS: str = Field(default="3344Frz@q0607")
    DB_NAME: str = Field(default="mess")
    
    # Конфигурация безопасности
    SECRET_KEY: str = Field(default="f8134dea6e71a1884d799b4a453ad93cbb7736358eceda96da85714c038d8635")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    
    # Настройки Uvicorn
    WS_HOST: str = Field(default="0.0.0.0")
    WS_PORT: int = Field(default=8000)

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    # !!! ИСПРАВЛЕНИЕ: Используем computed_field (вычисляемое поле)
    # Pydantic сам вызывает этот метод после инициализации, и результат сохраняется как атрибут.
    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

# Создаем единственный экземпляр настроек.
# DATABASE_URL теперь вычисляется внутри Settings().
settings = Settings()

# УДАЛИТЕ СТРОКИ 22-25 из оригинального кода!
# settings.DATABASE_URL = (...)