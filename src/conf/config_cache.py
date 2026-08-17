from typing import Any, Callable, Dict, Optional, Tuple

from fastapi.requests import Request
from fastapi.responses import Response
from fastapi_cache import FastAPICache
from passlib.context import CryptContext

pwd_context = CryptContext( schemes=[ "bcrypt" ], deprecated="auto" )


def custom_key_builder( func: Callable[ ..., Any ],
                        namespace: str = "",
                        *,
                        request: Optional[ Request ] = None,
                        response: Optional[ Response ] = None,
                        args: Tuple[ Any, ... ],
                        kwargs: Dict[ str, Any ], ) -> str:
	current_user = kwargs.get( "current_user" )
	contact_id = kwargs.get( "contact_id" )

	return (f"{namespace}:"
	        f"{func.__name__}:"
	        f"user:{current_user.id}:"
	        f"contact:{contact_id}")


async def invalidate_get_contact_repo_cache( current_user_id: int, contact_id: int, ):
	key = (f"{FastAPICache.get_prefix()}:"
	       f"contact_id:"
	       f"get_contact_by_id:"
	       f"user:{current_user_id}:"
	       f"contact:{contact_id}")

	backend = FastAPICache.get_backend()
	await backend.clear( key=key )
