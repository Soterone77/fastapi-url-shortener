from fastapi import (
    APIRouter,
    status,
    BackgroundTasks,
    Depends,
)

from api.api_v1.short_urls.crud import storage
from api.api_v1.short_urls.dependencies import (
    save_storage_state,
    api_token_or_user_basic_auth_required_for_unsafe_methods,
)
from schemas.short_url import ShortUrl, ShortUrlCreate, ShortUrlRead

router = APIRouter(
    prefix="/short-urls",
    tags=["Short URLs"],
    dependencies=[
        Depends(save_storage_state),
        Depends(api_token_or_user_basic_auth_required_for_unsafe_methods),
    ],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthenticated. Only for unsafe methods.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid API Token",
                    }
                }
            },
        }
    },
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
