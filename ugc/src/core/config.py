from _socket import gethostname

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    KAFKA_BROKER_HOST = Field('ugc.kafka', env='KAFKA_BROKER_HOST')
    KAFKA_BROKER_PORT = Field(9092, env='KAFKA_BROKER_PORT')
    KAFKA_TOPIC_PREFIX = "views"

    password: str = Field('', env='POSTGRES_PASSWORD')
    ugc_host: str = Field('0.0.0.0', env='DB_HOST')
    ugc_port: int = Field(8001, env='DB_PORT')

settings = Settings()

