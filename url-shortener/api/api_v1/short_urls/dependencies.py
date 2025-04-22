import logging
from netrc import NetrcParseError
from typing import Annotated

from fastapi import (
    HTTPException,
    BackgroundTasks,
    status,
    Request,
    Query,
)

from api.api_v1.short_urls.crud import storage
from core.config import API_TOKENS
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


def api_token_required_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        str,
        Query(),
    ] = "",
):
    if request.method not in UNSAFE_METHODS:
        return

    if not api_token or api_token not in API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token",
        )
