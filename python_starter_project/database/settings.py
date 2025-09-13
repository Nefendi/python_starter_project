from typing import TYPE_CHECKING

from pydantic_settings import BaseSettings, SettingsConfigDict

# An ugly workaround for this: https://github.com/pydantic/pydantic/issues/1490
if TYPE_CHECKING:
    PostgresDsn = str
else:
    from pydantic import PostgresDsn


class DbSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB_CONFIG_", case_sensitive=True)

    URL: PostgresDsn = (
        "postgresql+psycopg://python_starter_project:password"
        "@127.0.0.1:5432/python_starter_project"
    )
