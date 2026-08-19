import configparser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / "config.ini"

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

user = config.get("DEV_DB", "USER")
db_name = config.get("DEV_DB", "DB_NAME")
password = config.get("DEV_DB", "PASSWORD")
host = config.get("DEV_DB", "HOST")
port = config.get("DEV_DB", "PORT")