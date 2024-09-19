import asyncio
from typing import Annotated

from aiokafka import AIOKafkaProducer
from fastapi import Depends

from core.authentication.mail import MailClient
from kafka.producer import BrokerProducer
from core import settings


async def get_kafka_producer(topic: str) -> BrokerProducer:
    event_loop = asyncio.get_running_loop()
    return BrokerProducer(
        producer=AIOKafkaProducer(
            bootstrap_servers=settings.broker_config.url,
            loop=event_loop,
        ),
        email_topic=topic,
    )


async def get_client_email(
    broker_producer: BrokerProducer,
) -> MailClient:
    return MailClient(broker_producer=broker_producer, settings=settings)
