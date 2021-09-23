import asyncio

import pytest
from alembic import command
from alembic.config import Config
from fakeredis.aioredis import FakeRedis
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine


@pytest.fixture(scope="session", autouse=True)
def event_loop(request):
    """
    Creates asyncio event loop for each unit test session
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def flush_test_database():
    """
    Returns initialized database for each unit test session
    :return:
    """
    from core.config import DB_NAME, DB_PORT, DB_SERVICE, DB_HOST, DB_USER, DB_PASSWORD, DATABASE_URL, \
        ALEMBIC_UNIT_TEST_MIGRATIONS_DIR, ALEMBIC_ENV_FILE_DIR, ALEMBIC_INI_FILE_PATH

    engine = create_async_engine(f"{DB_SERVICE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres", echo=True,
                                 isolation_level='AUTOCOMMIT')

    async with engine.connect() as connection:
        await connection.execute(text(f"DROP DATABASE IF EXISTS {DB_NAME}"))
        await connection.execute(text(f"CREATE DATABASE {DB_NAME}"))

        alembic_cfg = Config(ALEMBIC_INI_FILE_PATH)
        alembic_cfg.set_main_option('sqlalchemy.url', DATABASE_URL.replace("+asyncpg", ""))
        alembic_cfg.set_main_option('script_location', ALEMBIC_ENV_FILE_DIR)
        alembic_cfg.set_main_option('version_locations', ALEMBIC_UNIT_TEST_MIGRATIONS_DIR)
        alembic_cfg.set_main_option('version_path_separator', ';')
        command.upgrade(alembic_cfg, "head")
        yield


@pytest.fixture
async def async_client() -> AsyncClient:
    """
    Creates http client for each unit test
    :return: AsyncClient
    """
    from core.main import app
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


@pytest.fixture(autouse=True)
async def transaction() -> AsyncSession:
    """
    Creates transaction for each test case. Then rollback it, if test success
    Django.TransactionTestCase analog
    """
    from core.db import transaction_atomic

    async with transaction_atomic() as transaction:
        yield transaction
        await transaction.rollback()


@pytest.fixture
def redis() -> FakeRedis:
    """
    Creates fake redis instance for each test case
    :return: FakeRedis
    """
    from core.redis import redis_connection
    return redis_connection
