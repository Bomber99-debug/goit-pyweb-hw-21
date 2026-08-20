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
	MAIL_BACKEND: str = "django.core.mail.backends.smtp.EmailBackend"
	MAIL_USER: str = "test"
	MAIL_PASSWORD: str = "123456"
	MAIL_FROM: str = "admin@web.com"
	MAIL_FROM_NAME: str = "TODO Test Email"
	EMAIL_HOST: str = "127.0.0.1"
	MAIL_PORT_SMTP: int = 1025
	MAIL_CONTAINER_PORT_SMTP: int = 1025
	MAIL_PORT_HTTP: int = 8025
	MAIL_CONTAINER_PORT_HTTP: int = 8025
	MAIL_HOST_USER: str = 'example@meta.ua'
	MAIL_HOST_PASSWORD: str = 'secretPassword'
	MAIL_USE_SSL: bool = False
	MAIL_USE_TLS: bool = False
	USE_CREDENTIALS: bool = True
	VALIDATE_CERTS: bool = True

	model_config = SettingsConfigDict( extra="ignore", env_file=BASE_DIR / ".env", env_file_encoding="utf-8" )


config = Settings()
