from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """ Класс базовых настроек """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )    

    # PosgreSQL поля для подключения, находятся в .env
    POSTGRES_USER: str = "postgress"
    POSTGRES_PASSWORD: str = "postgress"
    POSTGRES_DB: str = "DB-name"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432

    # SQL-логи
    ECHO_SQL: bool = False  

    # Собираемое значение для асинхронного подключения
    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        user = self.POSTGRES_USER  # используется для f-строки
        password = self.POSTGRES_PASSWORD
        return f"postgresql+asyncpg://{user}:{password}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Собираемое значение для синхронного подключения  
    @computed_field
    @property
    def SYNC_DATABASE_URL(self) -> str:
        user = self.POSTGRES_USER
        password = self.POSTGRES_PASSWORD
        return f"postgresql://{user}:{password}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    

settings = Settings()  