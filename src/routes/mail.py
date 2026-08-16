from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.email import RequestEmail
from src.services.auth import auth_service
from src.services.email import send_email
from src.database.db import get_db
from src.repository import email

router = APIRouter( prefix="/mail", tags=[ "mail" ] )


@router.get( "/confirmed_email/{token}" )
async def confirm_email( token: str, db: AsyncSession = Depends( get_db ) ):
	email = await auth_service.get_email_from_token( token )
	user = await email.get_user_by_email( email, db )
	if not user:
		raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error" )
	if user.confirmed:
		return { "message": "Email address already confirmed" }
	await email.confirm_email( email, db )
	return { "message": "Email address confirmed" }


@router.get( "/request_email" )
async def request_email( body: RequestEmail,
                         background_tasks: BackgroundTasks,
                         request: Request,
                         db: AsyncSession = Depends( get_db ), ):
	user = await email.get_user_by_email( body.email, db )
	if user.confirmed:
		return { "message": "Email address already confirmed" }
	if user:
		background_tasks.add_task( send_email, user.email, user.user_name, str( request.base_url ) )
	return { "message": "Email address confirmed" }
