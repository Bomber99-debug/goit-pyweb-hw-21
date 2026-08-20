from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path( __file__ ).resolve().parent.parent.parent


class Settings( BaseSettings ):
	""" DB connection config """
	POSTGRES_USER: str = "postgres"
	POSTGRES_PASSWORD: str = "123456"
	POSTGRES_HOST_IP: str = "127.0.0.1"
	POSTGRES_PORT: int = 5432
	POSTGRES_DB: str = "postgres"

	""" Mail config """

	EMAIL_BACKEND: str = "django.core.mail.backends.smtp.EmailBackend"
	EMAIL_HOST: str = "email"
	EMAIL_PORT: int = 1025

	EMAIL_HOST_USER: str = ""
	EMAIL_HOST_PASSWORD: str = ""

	EMAIL_USE_SSL: bool = False
	EMAIL_USE_TLS: bool = False

	DEFAULT_FROM_EMAIL: str = "admin@web.com"

	""" Django config """

	DJANGO_SECRET_KEY: str
	DJANGO_DEBUG: bool = True
	DJANGO_ALLOWED_HOSTS: str = "127.0.0.1,localhost"

	model_config = SettingsConfigDict( extra="ignore", env_file=BASE_DIR / ".env", env_file_encoding="utf-8" )


config = Settings()
