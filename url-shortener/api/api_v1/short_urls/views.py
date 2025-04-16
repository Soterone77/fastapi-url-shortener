from typing import Annotated
from annotated_types import Len
from fastapi import (
    APIRouter,
    Depends,
    status,
    Form,
)
from pydantic import AnyHttpUrl

from api.api_v1.short_urls.dependencies import (
    prefetch_short_url,
)
from api.api_v1.short_urls.crud import SHORT_URLS
from schemas.short_url import ShortUrl

router = APIRouter(
    prefix="/short-urls",
    tags=["Short URLs"],
)


@router.get("/", response_model=list[ShortUrl])
def read_short_urls_list():
    return SHORT_URLS


@router.get("/{slug}", response_model=ShortUrl)
def read_short_url_details(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_short_url),
    ],
) -> ShortUrl:
    return url


@router.post(
    "/",
    response_model=ShortUrl,
    status_code=status.HTTP_201_CREATED,
)
def create_short_url(
    target_url: Annotated[
        AnyHttpUrl,
        Form(),
    ],
    slug: Annotated[
        str,
        Len(min_length=3, max_length=10),
        Form(),
    ],
):

    return ShortUrl(
        target_url=target_url,
        slug=slug,
    )
