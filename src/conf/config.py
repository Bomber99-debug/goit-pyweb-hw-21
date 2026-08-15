from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings( BaseSettings ):
	DB_URL: str = "sqlite:///db.sqlite3"
	SECRET_KEY_JWT: str = ""
	ALGORITHM: str = "HS256"

	@field_validator( 'ALGORITHM' )
	@classmethod
	def validate_algorithm( cls, v: str ):
		if v not in [ "HS256", "HS384", "HS512" ]:
			raise ValueError( "Algorithm must be HS256 or HS384 or HS512" )
		return v

	model_config = SettingsConfigDict( extra='ignore', env_file='.env', env_file_encoding='utf-8' )


config = Settings()
