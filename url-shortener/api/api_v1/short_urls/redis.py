import secrets
from abc import ABC, abstractmethod

from redis import Redis
from core import config


class AbstractTokenHelper(ABC):
    """
    Что мне нужно от обертки?
    -проверять на наличие токена
    -добавлять токен в хранилище
    -сгенерировать и добавить токены
    """

    @abstractmethod
    def token_exist(
        self,
        token: str,
    ) -> bool:
        """
        Check if token exist
        :param token:
        :return:
        """

    @abstractmethod
    def add_token(
        self,
        token: str,
    ) -> None:
        """
        Save token to storage
        :param token:
        :return:
        """
        pass

    @classmethod
    def generate_token(cls) -> str:
        return secrets.token_urlsafe(16)

    def generate_and_save_token(
        self,
    ) -> str:
        token = self.generate_token()
        self.add_token(token)
        return token


class RedisTokenHelper(AbstractTokenHelper):

    def __init__(
        self,
        host: str,
        port: int,
        db: int,
        tokens_set_name: str,
    ) -> None:
        self.redis = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
        )
        self.tokens_set = tokens_set_name

    def token_exist(self, token: str) -> bool:
        return bool(
            self.redis.sismember(
                self.tokens_set,
                token,
            )
        )

    def add_token(self, token: str) -> None:
        self.redis.sadd(self.tokens_set, token)


redis_tokens = RedisTokenHelper(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_TOKENS,
    tokens_set_name=config.REDIS_TOKENS_SET_NAME,
)
