from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisDatabase(BaseModel):
    cache: int = 0


class RedisConfig(BaseModel):
    """Настройки для redis."""

    host: str = "localhost"
    port: int = 6379
    db: RedisDatabase = RedisDatabase()


class CacheNamespace(BaseModel):
    users: str = "users"


class CacheConfig(BaseModel):
    """Настройки для кэша."""

    prefix: str = "fastapi-cache"
    namespace: CacheNamespace = CacheNamespace()


class Database(BaseModel):
    """Поля для базы данных."""

    user: str
    password: str
    host: str
    port: int
    name: str
    echo: bool

    @property
    def url(self):
        """Построение URL."""
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.name}"
        )


class Settings(BaseSettings):
    """Основные настройки приложения."""

    app_name: str
    version: str
    host: str
    port: int
    debug: bool
    db: Database
    redis: RedisConfig = RedisConfig()
    cache: CacheConfig = CacheConfig()

    model_config = SettingsConfigDict(
        env_file=".env_example",
        env_nested_delimiter="__",
    )


settings = Settings()
