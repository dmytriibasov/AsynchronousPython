import os
import logging
import faker
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

from app.config import DB_URI
from app.models import Base
# from app.cve_records_repository import make_cve_record
from test import process_directory, insert_records_in_bulk

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

fake = faker.Faker()

DB_ECHO = os.environ.get("DB_ECHO", "false").lower() == "true"


def get_engine() -> AsyncEngine:
    print(DB_URI)
    return create_async_engine(
        DB_URI,
        echo=DB_ECHO,
    )


def make_session_class(engine: AsyncEngine) -> type[AsyncSession]:
    return async_sessionmaker(
        engine,
        expire_on_commit=False,
    )


async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def main():
    engine = get_engine()
    session_klass = make_session_class(engine)
    root = '/home/dmytriii/AsyncProgCourse/Homework_6/cves/cvelistV5/cves/1999'

    await create_tables(engine)

    async with session_klass() as session:
        logger.info("Creating CVEs")

        record_batch = []
        await process_directory(root, session, record_batch)

        # Insert any remaining records in the last batch
        if record_batch:
            await insert_records_in_bulk(record_batch, session)

        await session.flush()
        await session.commit()

    # async with session_klass() as session:
    #     logger.info("Fetching users")
    #     for user in await get_all_users(session):
    #         print(user)

    # await drop_tables(engine)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
