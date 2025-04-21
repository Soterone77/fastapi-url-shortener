from fastapi import (
    APIRouter,
    status,
)

from api.api_v1.short_urls.config import storage
from schemas.short_url import ShortUrl, ShortUrlCreate, ShortUrlRead

router = APIRouter(
    prefix="/short-urls",
    tags=["Short URLs"],
)


@router.get("/", response_model=list[ShortUrlRead])
def read_short_urls_list() -> list[ShortUrlRead]:
    return storage.get()


@router.post(
    "/",
    response_model=ShortUrlRead,
    status_code=status.HTTP_201_CREATED,
)
def create_short_url(
    short_url_create: ShortUrlCreate,
) -> ShortUrlRead:

    return storage.create(short_url_create)
