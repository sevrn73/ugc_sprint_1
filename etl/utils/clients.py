import json

from clickhouse_driver import Client
from kafka import KafkaConsumer

from utils.settings import settings

kafka_consumer = KafkaConsumer(
    settings.KAFKA_TOPIC_PREFIX,
    group_id='timestamp_movie',
    bootstrap_servers=f"{settings.KAFKA_BROKER_HOST}:{settings.KAFKA_BROKER_PORT}",
    enable_auto_commit=False,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

clickhouse_client = Client(
    host=settings.clickhouse_host,
    port=settings.clickhouse_port
)