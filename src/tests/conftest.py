import asyncio
import warnings

import pytest_asyncio
from httpx import AsyncClient

from src.main import app

warnings.filterwarnings("ignore", category=DeprecationWarning)


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_app():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        yield ac
