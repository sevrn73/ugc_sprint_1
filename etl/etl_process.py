import json
import time
import uuid
from clickhouse_driver import Client
from kafka import KafkaConsumer
from backoff import backoff
from settings import settings


def create_table(client) -> None:
    client.execute(
        """
        CREATE TABLE IF NOT EXISTS views (
            id String,
            user_id String,
            movie_id String,
            timestamp_movie Int64,
            time Int64
        ) Engine=MergeTree() ORDER BY id
        """
    )


def etl(kafka_consumer: KafkaConsumer, clickhouse_client: Client) -> None:
    data = []
    start = time.time()
    for message in kafka_consumer:
        msg = (
            str(uuid.uuid4()), 
            *str(message.key.decode('utf-8')).split(':'),
            message.value['timestamp_movie'],
            message.timestamp,
        )
        data.append(msg)
        if (len(data) == 1) or (time.time() - start >= 60):
            clickhouse_client.execute(
                "INSERT INTO views (id, user_id, movie_id, timestamp_movie, time) VALUES",
                data,
            )
            data = []
            start = time.time()
            kafka_consumer.commit()


@backoff()
def main() -> None:
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
    create_table(clickhouse_client)
    etl(kafka_consumer, clickhouse_client)


if __name__ == '__main__':
    main()