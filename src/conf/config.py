from pydantic import (
	ConfigDict,
	field_validator,
	EmailStr,
	)
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	DB_URL: str = "sqlite:///db.sqlite3"
	SECRET_KEY_JWT: str = ""
	ALGORITHM: str = "HS256"



config = Settings()
