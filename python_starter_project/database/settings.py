from pydantic import BaseSettings, PostgresDsn


class DbSettings(BaseSettings):
    URL: PostgresDsn = PostgresDsn(
        "postgresql://python-starter-project:password"
        "@127.0.0.1:5432/python-starter-project"
    )

    class Config:
        env_prefix = "DB_CONFIG_"
