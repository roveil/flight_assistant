from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import DATABASE_URL, TESTING
from core.utils import SingletonMeta


class UnitTestAsyncSession(AsyncSession, metaclass=SingletonMeta):
    """
    HACK! Per unit test transaction db connection. AsyncSession is singleton for unit tests.
    SessionMaker on __call__ creates and returns this class.
    """
    pass


engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=(UnitTestAsyncSession if TESTING else AsyncSession))


@asynccontextmanager
async def _unit_test_transaction_atomic() -> AsyncSession:
    """
    pytest_fixtures.transaction fixture opens a transaction and then rollback it after each test case
    This context manager returns this opened connection.
    :return: current unit test database connection with opened transaction
    """
    # Get our singleton database connection
    connection = async_session()
    yield connection


@asynccontextmanager
async def _transaction_atomic() -> AsyncSession:
    """
    Creates new database session and begin transaction
    :return: new connection with opened transaction
    """
    connection = async_session()

    try:
        async with connection.begin():
            yield connection
    finally:
        await connection.close()


transaction_atomic = _unit_test_transaction_atomic if TESTING else _transaction_atomic
