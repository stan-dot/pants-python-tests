from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings


class MySQLSettings(BaseSettings):
    database_url: str = Field(default="", alias="MYSQL_URL")
    user: str = Field(default="testuser", alias="MYSQL_USER")
    password: str = Field(default="testpassword", alias="MYSQL_PASSWORD")
    host: str = Field(default="localhost", alias="MYSQL_HOST")
    port: str = Field(default="3306", alias="MYSQL_PORT")
    db_name: str = Field(default="mydb", alias="MYSQL_DBNAME")
    use_dev: bool = Field(default=False, alias="MYSQL_USE_DEV")

    @property
    def effective_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        return f"mysql+aiomysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}?ssl=None"


class Settings(BaseSettings):
    """
    Configuration class for the application settings using Pydantic.
    Automatically loads variables from environment or .env files.
    """

    cors_origins: str = Field(
        default="http://localhost:3000",
        alias="CORS_ORIGINS",
    )
    environment: str = Field(default="", alias="ENVIRONMENT")
    mysql: MySQLSettings = Field(default_factory=MySQLSettings)

    @property
    def cors_origins_list(self) -> list[str]:
        return self.cors_origins.split(",")
