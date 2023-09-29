import logging

import toml
from pydantic import SecretStr
from pydantic_settings import BaseSettings

from es.utils.utils import get_project_root

logger = logging.getLogger(__name__)


class Database(BaseSettings):
    server: str
    database: str
    username: str
    password: SecretStr


class Config(BaseSettings):
    database: Database

    def __init__(self, **data):
        super().__init__(**data)


def load_config_from_toml(file_path):
    with open(file_path, "r") as toml_file:
        return Config(database=Database(**toml.load(toml_file)["database"]))


config_path = get_project_root() / "config.toml"
config = load_config_from_toml(config_path)

logger.info(f"Config loaded from {config_path}")
