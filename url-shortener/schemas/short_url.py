from typing import Annotated

from annotated_types import Len, MaxLen
from pydantic import BaseModel, AnyHttpUrl


DescriptionString = Annotated[
    str,
    MaxLen(200),
]


class ShortUrlBase(BaseModel):
    target_url: AnyHttpUrl
    description: DescriptionString = ""


class ShortUrl(ShortUrlBase):
    """
    Модель сокращенной ссылки
    """

    slug: str
    visits: int = 42


class ShortUrlRead(ShortUrlBase):
    """
    Модель для чтения данных по сокращенной ссылке.
    """

    slug: str


class ShortUrlUpdate(ShortUrlBase):
    """
    Модель для обновления информации о сокращенной ссылке
    """

    description: DescriptionString


class ShortUrlPartialUpdate(ShortUrlBase):
    """
    Модель для частичного обновления информации
    о сокращенной ссылке
    """

    target_url: AnyHttpUrl | None = None

    description: DescriptionString | None = None


class ShortUrlCreate(ShortUrlBase):
    """
    Модель для создания сокращенной ссылки
    """

    slug: Annotated[
        str,
        Len(min_length=3, max_length=10),
    ]
