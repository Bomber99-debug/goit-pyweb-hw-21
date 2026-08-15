"""Завантаження параметрів підключення до бази даних із config.ini."""

import configparser
from pathlib import Path


BASE_DIR: Path = Path(__file__).resolve().parent
CONFIG_FILE: Path = BASE_DIR / "config.ini"

config_parser = configparser.ConfigParser()
config_parser.read(CONFIG_FILE)

db_user: str = config_parser.get("DEV_DB", "USER")
db_name: str = config_parser.get("DEV_DB", "DB_NAME")
db_password: str = config_parser.get("DEV_DB", "PASSWORD")
db_host: str = config_parser.get("DEV_DB", "HOST")
db_port: str = config_parser.get("DEV_DB", "PORT")