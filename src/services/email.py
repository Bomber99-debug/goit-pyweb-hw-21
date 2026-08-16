from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr, NameEmail

from src.services.auth import auth_service
from src.conf.config import config

mail_config = ConnectionConfig( MAIL_USERNAME=config.MAIL_USER,
                                MAIL_PASSWORD=config.MAIL_PASSWORD,
                                MAIL_FROM=config.MAIL_FROM,
                                MAIL_PORT=config.MAIL_PORT,
                                MAIL_SERVER=config.MAIL_HOST_IP,
                                MAIL_STARTTLS=config.MAIL_STARTTLS,
                                MAIL_SSL_TLS=config.MAIL_SSL_TLS,
                                USE_CREDENTIALS=config.USE_CREDENTIALS, )


async def send_email( email: EmailStr, username: str, host: str ):
	try:
		token_verification = auth_service.create_email_token( { "sub": email } )
		message = MessageSchema( subject="Email Verification",
		                         recipients=[ NameEmail(name=username, email=email) ],
		                         template_body={ "host": host, "username": username, "token": token_verification },
		                         subtype=MessageType.html, )
		fm = FastMail( config=mail_config )
		await fm.send_message( message, template_name="verify_email.html" )
	except ConnectionError as err:
		print( err )
