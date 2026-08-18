from typing import Any, Callable, Dict, Optional, Tuple

from fastapi.requests import Request
from fastapi.responses import Response
from fastapi_cache import FastAPICache
from passlib.context import CryptContext

pwd_context = CryptContext( schemes=[ "bcrypt" ], deprecated="auto" )

def custom_login_key_builder( func: Callable[ ..., Any ],
                                 namespace: str = "",
                                 *,
                                 request: Optional[ Request ] = None,
                                 response: Optional[ Response ] = None,
                                 args: Tuple[ Any, ... ],
                                 kwargs: Dict[ str, Any ], ) -> str:
	body = kwargs.get("body")
	print(f"kwargs:{kwargs}")
	return (f"body:{body}")

def custom_contacts_key_builder( func: Callable[ ..., Any ],
                                 namespace: str = "",
                                 *,
                                 request: Optional[ Request ] = None,
                                 response: Optional[ Response ] = None,
                                 args: Tuple[ Any, ... ],
                                 kwargs: Dict[ str, Any ], ) -> str:
	current_user = kwargs.get( "current_user" )
	limit = kwargs.get( "limit" )
	offset = kwargs.get( "offset" )
	return (f"{namespace}:"
	        f"{func.__name__}:"
	        f"user:{current_user.id}:"
	        f"limit:{limit}"
	        f"offset:{offset}")


def custom_contact_key_builder( func: Callable[ ..., Any ],
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


def custom_phones_key_builder( func: Callable[ ..., Any ],
                               namespace: str = "",
                               *,
                               request: Optional[ Request ] = None,
                               response: Optional[ Response ] = None,
                               args: Tuple[ Any, ... ],
                               kwargs: Dict[ str, Any ], ) -> str:
	current_user = kwargs.get( "current_user" )
	limit = kwargs.get( "limit" )
	offset = kwargs.get( "offset" )
	return (f"{namespace}:"
	        f"{func.__name__}:"
	        f"user:{current_user.id}:"
	        f"limit:{limit}"
	        f"offset:{offset}")


def custom_phone_key_builder( func: Callable[ ..., Any ],
                              namespace: str = "",
                              *,
                              request: Optional[ Request ] = None,
                              response: Optional[ Response ] = None,
                              args: Tuple[ Any, ... ],
                              kwargs: Dict[ str, Any ], ) -> str:
	current_user = kwargs.get( "current_user" )
	phone_id = kwargs.get( "phone_id" )
	return (f"{namespace}:"
	        f"{func.__name__}:"
	        f"user:{current_user.id}:"
	        f"phone:{phone_id}")


async def invalidate_get_phone_repo_cache( current_user_id: int, phone_id: int, ):
	key = (f"{FastAPICache.get_prefix()}:"
	       f"contact_id:"
	       f"get_contact_by_id:"
	       f"user:{current_user_id}:"
	       f"contact:{phone_id}")

	backend = FastAPICache.get_backend()
	await backend.clear( key=key )


def custom_search_key_builder( func: Callable[ ..., Any ],
                               namespace: str = "",
                               *,
                               request: Optional[ Request ] = None,
                               response: Optional[ Response ] = None,
                               args: Tuple[ Any, ... ],
                               kwargs: Dict[ str, Any ], ) -> str:
	current_user = kwargs.get( "current_user" )
	return (f"{namespace}:"
	        f"{func.__name__}:"
	        f"user:{current_user.id}")
