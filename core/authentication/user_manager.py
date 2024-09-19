import os
import logging
from typing import Optional

from fastapi import Request, Response, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, models

from core import User
from core import settings
from core.authentication.mail import MailClient
from core.types.user_id import UserIdType
# from dependencies.authentication.mail_client import get_mail_client
from dependencies.broker_producer import get_client_email
from dependencies.broker_producer import get_kafka_producer
from kafka.producer import BrokerProducer


log = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[User, UserIdType]):
    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret

    async def on_after_register(
        self,
        user: User,
        request: Optional["Request"] = None,
    ):
        log.warning(
            "User %r has registered.",
            user.id,
        )

    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request: Optional[Request] = None,
    ):
        log.warning(
            "Verification requested for user %r. Verification token: %r",
            user.id,
            token,
        )

        producer: BrokerProducer = await get_kafka_producer(topic=settings.broker_config.verify_email)
        mail_client: MailClient = await get_client_email(
            broker_producer=producer,
        )
        await mail_client.send_verify_email(to=user.email, token=token)

    async def on_after_verify(
        self, user: models.UP, request: Optional[Request] = None
    ) -> None:
        log.warning(
            "User %r has been verified.",
            user.id,
        )

    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: Optional[Request] = None,
    ):
        log.warning(
            "User %r has forgot their password. Reset token: %r",
            user.id,
            token,
        )

    async def on_after_login(
        self,
        user: User,
        request: Optional[Request] = None,
        response: Optional[Response] = None,
    ):
        log.warning(
            f"User %r has logged in. {os.getpid()}",
            user.id,
        )

        producer: BrokerProducer = await get_kafka_producer(topic=settings.broker_config.email_topic)
        mail_client: MailClient = await get_client_email(
            broker_producer=producer,
        )
        await mail_client.send_welcome_email(to=user.email)
