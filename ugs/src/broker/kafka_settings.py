from aiokafka import AIOKafkaProducer

from core.config import settings

class KafkaProducer:
    kafka_producer = None

    async def get_producer(self):
        self.kafka_producer = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_CONSUMER_SETTINGS["bootstrap.servers"],
            )
        await self.kafka_producer.start()

    async def stop_producer(self,):
        await self.kafka_producer.start()

kafka = KafkaProducer()