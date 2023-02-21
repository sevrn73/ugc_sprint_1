from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    service_url: str = Field("http://ugc_api:8001", env="SERVICE_URL")
