import logging

from pydantic import BaseModel, AnyHttpUrl, ValidationError

from core.config import SHORTS_URLS_STORAGE_FILEPATH
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlUpdate,
    ShortUrlPartialUpdate,
)

log = logging.getLogger(__name__)


class ShortUrlsStorage(BaseModel):
    slug_to_short_url: dict[str, ShortUrl] = {}

    def save_state(self) -> None:
        SHORTS_URLS_STORAGE_FILEPATH.write_text(self.model_dump_json(indent=2))
        log.info("Saved short urls to storage file.")

    @classmethod
    def from_state(cls) -> "ShortUrlsStorage":
        if not SHORTS_URLS_STORAGE_FILEPATH.exists():
            log.info("Shorts urls storage doesn't exist.")
            return ShortUrlsStorage()
        return cls.model_validate_json(SHORTS_URLS_STORAGE_FILEPATH.read_text())

    def init_storage_from_state(self) -> None:
        try:
            data = ShortUrlsStorage.from_state()
        except ValidationError:
            self.save_state()
            log.warning("Rewritten storage file due to validation error")
            return
        # мы обновляем свойство напрямую,
        # если будут новые свойства,
        # то мы тоже хотим их обновить.

        self.slug_to_short_url.update(
            data.slug_to_short_url,
        )
        log.warning("Recovered data from storage file")

    def get(self) -> list[ShortUrl]:
        return list(self.slug_to_short_url.values())

    def get_by_slug(self, slug: str) -> ShortUrl | None:
        return self.slug_to_short_url.get(slug)

    def create(self, short_url_in: ShortUrlCreate) -> ShortUrl:
        short_url = ShortUrl(**short_url_in.model_dump())
        self.slug_to_short_url[short_url.slug] = short_url
        log.info("Created short url %s", short_url)
        return short_url

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_short_url.pop(slug, None)

    def delete(self, short_url: ShortUrl) -> None:
        self.delete_by_slug(slug=short_url.slug)

    def update(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlUpdate,
    ) -> ShortUrl:
        # updated_short_url = short_url.model_copy(
        #     update=short_url_in.model_dump(),
        # )
        # self.slug_to_short_url[updated_short_url.slug] = updated_short_url
        # return updated_short_url
        for field_name, value in short_url_in:
            setattr(short_url, field_name, value)
        # self.slug_to_short_url[short_url.slug] = short_url
        return short_url

    def update_partial(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlPartialUpdate,
    ):
        for field_name, value in short_url_in.model_dump(exclude_unset=True).items():
            setattr(short_url, field_name, value)
        return short_url


storage = ShortUrlsStorage()


# storage.create(
#     ShortUrlCreate(
#         target_url=AnyHttpUrl("https://www.example.com"),
#         slug="example",
#     )
# )
#
# storage.create(
#     ShortUrlCreate(
#         target_url=AnyHttpUrl("https://www.google.com"),
#         slug="search",
#     )
# )
