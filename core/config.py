# from typing import Dict

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn


class DataBase(BaseModel):
    url: PostgresDsn
    echo: bool = True
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class RedisConfig(BaseModel):
    host: str
    port: int
    db: str


class AccessToken(BaseModel):
    lifetime_seconds: int = 3600
    reset_password_token_secret: str
    verification_token_secret: str


class BrokerConfig(BaseModel):
    url: str
    email_topic: str
    callback_topic: str = "callback_email_topic"
    verify_email: str = "verify_email_topic"


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    auth: str = "/auth"
    users: str = "/users"
    products: str = "/products"
    messages: str = "/messages"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()
    
    @property
    def bearer_token_url(self) -> str:
        parts = (self.prefix, self.v1.prefix, self.v1.auth, "/login")
        path = "".join(parts)
        return path[1:]


class RunConfig(BaseModel):
    app: str = "main:main_app"
    reload: bool = True
    host: str = "0.0.0.0"
    port: int = 8000


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # 1 env перезаписывает другой
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        #  разделитель вложенности объекта
        env_nested_delimiter="__",
        env_prefix="FASTAPI__"
    )
    config: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    access_token: AccessToken
    db: DataBase
    redis: RedisConfig
    broker_config: BrokerConfig


settings = Settings()
