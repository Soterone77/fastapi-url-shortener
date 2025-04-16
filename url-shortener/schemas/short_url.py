from pydantic import BaseModel, HttpUrl, AnyHttpUrl


class ShortUrlBase(BaseModel):
    target_url: AnyHttpUrl
    slug: str


class ShortUrl(ShortUrlBase):
    """
    Модель сокращенной ссылки
    """
