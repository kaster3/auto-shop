import json

from aiokafka import AIOKafkaConsumer

from kafka.consumer import BrokerConsumer
from core import settings


def get_broker_consumer() -> BrokerConsumer:
    print(settings.broker_config.url)
    return BrokerConsumer(
        consumer=AIOKafkaConsumer(
            settings.broker_config.callback_topic,
            bootstrap_servers=settings.broker_config.url,
            value_deserializer=lambda message: json.loads(message.decode("utf-8")),
        ),
        email_callback_topic=settings.broker_config.callback_topic,
    )
