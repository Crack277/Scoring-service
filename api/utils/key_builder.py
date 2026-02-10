import hashlib

from fastapi import Response, Request
from typing import Any, Callable, Tuple, Dict, Optional

from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase


def users_key_builder(
    func: Callable[..., Any],
    namespace: str = "",
    *,
    request: Optional[Request] = None,
    response: Optional[Request] = None,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
) -> str:
    exclude_types = (SQLAlchemyUserDatabase,)
    cache_kwargs = {}
    for name, value in cache_kwargs:
        if isinstance(value, exclude_types):
            continue
        cache_kwargs[name] = value

    cache_key = hashlib.md5(
        f"{func.__module__}:{func.__name__}:{args}:{cache_kwargs}".encode()
    ).hexdigest()
    return f"{namespace}:{cache_key}"
