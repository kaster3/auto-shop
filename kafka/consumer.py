import asyncio
import logging
from dataclasses import dataclass

from aiokafka import AIOKafkaConsumer


@dataclass
class BrokerConsumer:
    consumer: AIOKafkaConsumer
    email_callback_topic: str

    async def open_connection(self) -> None:
        logging.info("Attempting to start Kafka consumer with timeout")
        try:
            await asyncio.wait_for(self.consumer.start(), timeout=10.0)
            logging.info("Kafka consumer started successfully")
        except asyncio.TimeoutError:
            logging.error("Timeout occurred while starting Kafka consumer")

    async def close_connection(self) -> None:
        await self.consumer.stop()

    async def consume_callback_message(self) -> None:
        await self.open_connection()
        print("Waiting for messages on topic:", self.email_callback_topic)
        try:
            async for message in self.consumer:
                print(message.value)
        finally:
            print("Closing Kafka consumer")
            await self.close_connection()
