from aiokafka import AIOKafkaProducer
import asyncio
import json

producer = AIOKafkaProducer(
    bootstrap_servers="localhost:9092"
)

async def start_kafka():
    await producer.start()

async def stop_kafka():
    await producer.stop()

async def publish_event(topic: str, data: dict):
    await producer.send_and_wait(topic, json.dumps(data).encode())



class KafkaProducerManager:
    def __init__(self, bootstrap_servers):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=bootstrap_servers
        )

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def publish(self, topic: str, message: bytes):
        await self.producer.send_and_wait(topic, message)