"""
Модуль ETL процесса
"""
import json
import time
import uuid

from clickhouse_driver import Client
from kafka import KafkaConsumer

from utils.backoff import backoff
from utils.clients import get_kafka, get_clickhouse


def create_table(client: Client) -> None:
    """
    Создание таблицы в Clickhouse

    :param client: клиент Clickhouse
    """
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
    """
    ETL процесс, переносит данные из Kafka в Clickhouse

    :param kafka_consumer: консьюмер кафки
    :param clickhouse_client: клиент Clickhouse
    """
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
        if (len(data) >= 1) or (time.time() - start >= 60):
            clickhouse_client.execute(
                "INSERT INTO views (id, user_id, movie_id, timestamp_movie, time) VALUES",
                data,
            )
            data = []
            start = time.time()
            kafka_consumer.commit()


@backoff()
def main() -> None:
    """
    Основная функция ETL процесса
    """
    kafka_consumer = get_kafka()
    clickhouse_client = get_clickhouse()
    create_table(clickhouse_client)
    etl(kafka_consumer, clickhouse_client)



if __name__ == '__main__':
    main()