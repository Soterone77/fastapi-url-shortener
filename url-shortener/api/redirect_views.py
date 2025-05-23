from typing import Annotated

from fastapi import Depends, APIRouter
from starlette.responses import RedirectResponse

from api.api_v1.short_urls.dependencies import prefetch_short_url
from schemas.short_url import (
    ShortUrl,
    ShortUrlRead,
)

router = APIRouter(
    prefix="/r",
    tags=["Redirect"],
)


@router.get("/{slug}")
@router.get("/{slug}/")
def redirect_short_url(
    url: Annotated[
        ShortUrlRead,
        Depends(prefetch_short_url),
    ],
):
    return RedirectResponse(
        url=str(url.target_url),
    )
