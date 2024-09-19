import json
import uuid
from dataclasses import dataclass

import aio_pika

from core.config import Settings
from kafka.producer import BrokerProducer


@dataclass
class MailClient:
    settings: Settings
    broker_producer: BrokerProducer

    async def send_welcome_email(self, to: str) -> None:

        email_body = {
            "message": "Welcome to our service!",
            "user_email": to,
            "subject": "Welcome message",
            "correlation_id": str(uuid.uuid4()),
        }

        await self.broker_producer.send_welcome_email(email_data=email_body)

    async def send_verify_email(self, to: str, token: str) -> None:

        email_body = {
            "message": "Verify message",
            "user_email": to,
            "subject": f"Please Verify your email by clicking this link http://127.0.0.1:8000/api/v1/auth/verify?token={token}",
            "correlation_id": str(uuid.uuid4()),
        }

        await self.broker_producer.send_welcome_email(email_data=email_body)



# @dataclass
# class MailClient:
#     settings: Settings
#
#     async def send_welcome_email(self, to: str) -> None:
#         connection = await aio_pika.connect_robust(
#             self.settings.amqp_url
#         )  # "amqp://guest:guest@localhost:5672//"
#
#         email_body = {
#             "message": "Welcome to our service!",
#             "user_email": to,
#             "subject": "Welcome message",
#         }
#         async with connection:
#             channel = await connection.channel()
#             await channel.declare_queue("email_queue", durable=True)
#             message = aio_pika.Message(
#                 body=json.dumps(email_body).encode(),
#                 correlation_id=str(uuid.uuid4()),
#             )
#
#             await channel.default_exchange.publish(
#                 message=message,
#                 routing_key="email_queue",
#             )
