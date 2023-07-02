from typing import TYPE_CHECKING

from pydantic import BaseSettings

# An ugly workaround for this: https://github.com/pydantic/pydantic/issues/1490
if TYPE_CHECKING:
    PostgresDsn = str
else:
    from pydantic import PostgresDsn


class DbSettings(BaseSettings):
    URL: PostgresDsn = (
        "postgresql://python_starter_project:password"
        "@127.0.0.1:5432/python_starter_project"
    )

    class Config:
        env_prefix = "DB_CONFIG_"
        case_sensitive = True
