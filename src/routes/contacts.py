from collections.abc import Sequence  # noqa: EXE002

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.entity.models import Contact, User
from src.repository import contacts as contact_repository
from src.repository import phones as phones_repository
from src.schemas.contacts import (
    ContactCreateSchema,
    ContactResponseSchema,
    ContactUpdateSchema,
)
from src.services.auth import auth_service

router = APIRouter(
    prefix="/contacts",
    tags=["contacts"],
)


@router.get(
    "/",
    response_model=list[ContactResponseSchema],
)
async def get_contacts(
    limit: int = Query(default=10, ge=10, le=100),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
) -> Sequence[Contact]:
    """Повертає список контактів з урахуванням пагінації."""

    contact_list = await contact_repository.get_contacts(
        db=db, skip=offset, limit=limit, user=current_user
    )

    if contact_list is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )

    return contact_list


@router.get(
    "/{contact_id}",
    response_model=ContactResponseSchema,
)
async def get_contact_by_id(
    db: AsyncSession = Depends(get_db),
    contact_id: int = Path(ge=1),
    current_user: User = Depends(auth_service.get_current_user),
) -> Contact:
    """Повертає контакт за його ідентифікатором."""

    contact = await contact_repository.get_contact_by_id(
        db=db, contact_id=contact_id, user=current_user
    )

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )

    return contact


@router.post(
    "/",
    response_model=ContactCreateSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_contact(
    contact_data: ContactCreateSchema,
    db: AsyncSession = Depends(get_db),  # noqa: B008
    current_user: User = Depends(auth_service.get_current_user),  # noqa: B008
) -> Contact:
    """Створює новий контакт."""

    for phone_data in contact_data.phones:
        phone = await phones_repository.get_phone_by_number(
            db=db,
            phone_number=phone_data.number,
            user=current_user
        )
        if phone is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Phone already exists",
            )

    contact = await contact_repository.create_contact(
        db=db, contact_data=contact_data, user=current_user
    )

    return contact


@router.put(
    "/{contact_id}",
    response_model=ContactUpdateSchema,
)
async def update_contact(
    contact_data: ContactUpdateSchema,
    contact_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),  # noqa: B008
    current_user: User = Depends(auth_service.get_current_user),  # noqa: B008
) -> Contact:
    """Оновлює контакт за його ідентифікатором."""

    for phone_data in contact_data.phones:
        phone = await phones_repository.get_phone_by_number(
            db=db, phone_number=phone_data.number, user=current_user
        )
        if phone is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Phone already exists",
            )

    contact = await contact_repository.update_contact(
        db=db, contact_data=contact_data, contact_id=contact_id, user=current_user
    )

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )

    return contact


@router.delete(
    "/{contact_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_contact(
    db: AsyncSession = Depends(get_db),
    contact_id: int = Path(ge=1),
    current_user: User = Depends(auth_service.get_current_user),
) -> None:
    """Видаляє контакт за його ідентифікатором."""

    await contact_repository.delete_contact(
        db=db, contact_id=contact_id, user=current_user
    )
