from _socket import gethostname

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    KAFKA_BROKER_HOST = Field('ugs.kafka', env='KAFKA_BROKER_HOST')
    KAFKA_BROKER_PORT = Field(9092, env='KAFKA_BROKER_PORT')
    #KAFKA_BROKER_URL = f"{KAFKA_BROKER_HOST}:{KAFKA_BROKER_PORT}"
    KAFKA_BROKER_URL = f"ugs.kafka:{9092}"
    KAFKA_TOPIC_PREFIX = "GpnDs.HDWS."
    KAFKA_TOPIC_GROUP = KAFKA_TOPIC_PREFIX + "group." + gethostname()
    KAFKA_CONSUMER_SETTINGS = {
        "bootstrap.servers": KAFKA_BROKER_URL,
        "client.id": "GpnDs.HDWS.Worker",
        "group.id": KAFKA_TOPIC_GROUP,
        "auto.offset.reset": "latest",
        "enable.auto.commit": True,
        "session.timeout.ms": 10000,
        "heartbeat.interval.ms": 3000,
    }
    KAFKA_TOPIC_POSTFIX = ""
    KAFKA_NOTIFICATION_TOPIC = KAFKA_TOPIC_PREFIX + "Notifications" + KAFKA_TOPIC_POSTFIX

    password: str = Field('', env='POSTGRES_PASSWORD')
    ugs_host: str = Field('0.0.0.0', env='DB_HOST')
    ugs_port: int = Field(8001, env='DB_PORT')
    jwt_secret_key: str = 'top_secret'

settings = Settings()

