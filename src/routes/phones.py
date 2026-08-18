from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from fastapi_cache.decorator import cache
from pyrate_limiter import Duration, Limiter, Rate
from sqlalchemy.ext.asyncio import AsyncSession

from src.conf.config_cache import custom_phone_key_builder, custom_phones_key_builder, invalidate_get_phone_repo_cache
from src.database.db import get_db
from src.entity.models import Phone, User
from src.repository import phones as phones_repository
from src.schemas.contacts import (PhoneCreateSchema, PhoneResponseSchema, PhoneUpdateSchema)
from src.services.auth import auth_service
from src.services.rate_limiter import RateLimiter

router = APIRouter( prefix="/phone", tags=[ "phone" ], )


@router.get( "/",
             response_model=list[ PhoneResponseSchema ],
             dependencies=[ Depends( RateLimiter( limiter=Limiter( Rate( 1, Duration.SECOND * 5, ), ), ), ), ], )
@cache( expire=60, namespace="phone_id", key_builder=custom_phones_key_builder )
async def get_phones( limit: int = Query( default=10, ge=10, le=100 ),
                      offset: int = Query( default=0, ge=0 ),
                      db: AsyncSession = Depends( get_db ),
                      current_user: User = Depends( auth_service.get_current_user ), ) -> Sequence[ Phone ]:
	"""Повертає список телефонних номерів з урахуванням пагінації."""

	phone_list = await phones_repository.get_phones( db=db, skip=offset, limit=limit, user=current_user, )

	if phone_list is None:
		raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="Phone not found", )

	return phone_list


@router.get( "/{phone_id}",
             response_model=PhoneResponseSchema,
             dependencies=[ Depends( RateLimiter( limiter=Limiter( Rate( 1, Duration.SECOND * 5, ), ), ), ), ], )
@cache( expire=60, namespace="phone_id", key_builder=custom_phone_key_builder )
async def get_phone_by_id( db: AsyncSession = Depends( get_db ),
                           phone_id: int = Path( ge=1 ),
                           current_user: User = Depends( auth_service.get_current_user ), ) -> Phone:
	"""Повертає телефонний номер за його ідентифікатором."""

	phone = await phones_repository.get_phone_by_id( db=db, phone_id=phone_id, user=current_user, )

	if phone is None:
		raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="Phone not found", )

	return phone


@router.post( "/", response_model=PhoneCreateSchema, status_code=status.HTTP_201_CREATED, )
async def create_phone( phone_data: PhoneCreateSchema,
                        db: AsyncSession = Depends( get_db ),
                        current_user: User = Depends( auth_service.get_current_user ), ) -> Phone:
	"""Створює новий телефонний номер."""

	phone = await phones_repository.get_phone_by_number( db=db, phone_number=phone_data.number, user=current_user, )
	if phone is not None:
		raise HTTPException( status_code=status.HTTP_409_CONFLICT, detail="Phone already exists", )

	phone = await phones_repository.create_phone( db=db, phone_data=phone_data, user=current_user, )

	return phone


@router.put( "/{phone_id}", response_model=PhoneUpdateSchema, )
async def update_phone( phone_data: PhoneUpdateSchema,
                        phone_id: int = Path( ge=1 ),
                        db: AsyncSession = Depends( get_db ),
                        current_user: User = Depends( auth_service.get_current_user ), ) -> Phone:
	"""Оновлює телефонний номер за його ідентифікатором."""

	phone = await phones_repository.get_phone_by_number( db=db, phone_number=phone_data.number, user=current_user, )
	if phone is not None:
		raise HTTPException( status_code=status.HTTP_409_CONFLICT, detail="Phone already exists", )

	phone = await phones_repository.update_phone( db=db, phone_data=phone_data, phone_id=phone_id, user=current_user, )

	if phone is None:
		raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="Phone not found", )

	await invalidate_get_phone_repo_cache( current_user_id=current_user.id, phone_id=phone_id )

	return phone


@router.delete( "/{phone_id}", status_code=status.HTTP_204_NO_CONTENT, )
async def delete_phone( db: AsyncSession = Depends( get_db ),
                        phone_id: int = Path( ge=1 ),
                        current_user: User = Depends( auth_service.get_current_user ), ) -> None:
	"""Видаляє телефонний номер за його ідентифікатором."""

	await invalidate_get_phone_repo_cache( current_user_id=current_user.id, phone_id=phone_id )

	await phones_repository.delete_phone( db=db, phone_id=phone_id, user=current_user )
