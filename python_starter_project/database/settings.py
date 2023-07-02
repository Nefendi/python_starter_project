from pydantic import BaseSettings, Field, PostgresDsn


class DbSettings(BaseSettings):
    URL: PostgresDsn = Field(
        default=(
            "postgresql://python_starter_project:password"
            "@127.0.0.1:5432/python_starter_project"
        )
    )

    class Config:
        env_prefix = "DB_CONFIG_"
