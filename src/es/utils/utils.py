import logging
from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent.parent


def get_module_root() -> Path:
    return Path(__file__).parent.parent
