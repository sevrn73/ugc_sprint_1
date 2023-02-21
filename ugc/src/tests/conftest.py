import asyncio
from dataclasses import dataclass
from typing import Union

import aiohttp
import pytest
import pytest_asyncio
from multidict import CIMultiDictProxy

from .settings import TestSettings

settings = TestSettings()

def pytest_collection_modifyitems(items):
    for item in items:
        item.add_marker('asyncio')

@dataclass
class HTTPResponse:
    body: Union[dict, str]
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(name="event_loop", scope="session")
def event_loop() -> asyncio.AbstractEventLoop:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def http_client():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture(scope="module")
def make_post_request(http_client):
    async def inner(
        method: str, data: dict = None, headers: dict = None
    ) -> HTTPResponse:
        data = data or {}
        url = f"{settings.service_url}/ugc_api/v1/{method}"
        async with http_client.post(url, data=data, headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )
    return inner




