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
	params = kwargs.copy()
	params.pop( 'db', None )
	if 'current_user' in params:
		params[ 'current_user' ] = params[ 'current_user' ].id
	key_parts = [ namespace, func.__name__ ] + [ f"{k}:{v}" for k, v in params.items() ]
	return ":".join( key_parts )


async def invalidate_get_contact_repo_cech( current_user_id, contact_id ):
	print( f"fastapi-cache:contact_id:get_contact_by_id:"
	       f"current_user:{current_user_id}:"
	       f"contact_id:{contact_id}", )
	await FastAPICache.clear( namespace=f"fastapi-cache:contact_id:get_contact_by_id:"
	                                    f"current_user:{current_user_id}:"
	                                    f"contact_id:{contact_id}", )
