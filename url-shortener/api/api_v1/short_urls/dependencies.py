import logging
from netrc import NetrcParseError
from typing import Annotated

from fastapi import (
    HTTPException,
    BackgroundTasks,
    status,
    Request,
)
from fastapi.params import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    HTTPBasic,
    HTTPBasicCredentials,
)
from api.api_v1.short_urls.crud import storage
from .redis import redis_tokens
from core.config import (
    API_TOKENS,
    USER_DB,
    REDIS_TOKENS_SET_NAME,
)
from schemas.short_url import ShortUrl

log = logging.getLogger(__name__)

UNSAFE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "DELETE",
        "PATCH",
    }
)

static_api_token = HTTPBearer(
    scheme_name="Static API token",
    description="Your **Static API token** from developer portal. [Read more](#)",
    auto_error=False,
)
user_basic_auth = HTTPBasic(
    scheme_name="Basic Auth",
    description="Basic username + password auth",
    auto_error=False,
)


def prefetch_short_url(slug: str) -> ShortUrl:
    url: ShortUrl | None = storage.get_by_slug(slug=slug)
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"URL {slug!r} not found",
    )


def save_storage_state(
    request: Request,
    background_tasks: BackgroundTasks,
):
    # исполнение кода до входа внутрь view функции
    yield
    # исполнение кода после покидания view функции
    if request.method in UNSAFE_METHODS:
        log.info("Add background task to  save storage")
        background_tasks.add_task(storage.save_state)


def validate_api_token(
    api_token: HTTPAuthorizationCredentials,
):
    if redis_tokens.sismember(
        REDIS_TOKENS_SET_NAME,
        api_token.credentials,
    ):
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API token",
    )


def api_token_required_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
):
    log.info("API token: %s ", api_token)

    if request.method not in UNSAFE_METHODS:
        return

    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API token is required",
        )

    validate_api_token(api_token=api_token)


def validate_basic_auth(
    credentials: HTTPBasicCredentials | None,
):
    if (
        credentials
        and credentials.username in USER_DB
        and credentials.password == USER_DB[credentials.username]
    ):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password.",
        headers={"WWW-Authenticate": "Basic"},
    )


def user_basic_auth_required_for_unsafe_methods(
    request: Request,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ] = None,
):

    if request.method not in UNSAFE_METHODS:
        return

    validate_basic_auth(
        credentials=credentials,
    )


def api_token_or_user_basic_auth_required_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ] = None,
):
    if request.method not in UNSAFE_METHODS:
        return

    if credentials:
        return validate_basic_auth(credentials=credentials)

    if api_token:
        return validate_api_token(api_token=api_token)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="API token or basic auth is required",
    )
