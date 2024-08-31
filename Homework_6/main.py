import os
import logging
import sys

import faker
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

from app.config import DB_URI
from app.models import Base
from app.processor import CveDataProcessor


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

fake = faker.Faker()

DB_ECHO = os.environ.get("DB_ECHO", "false").lower() == "true"


def get_engine() -> AsyncEngine:
    return create_async_engine(DB_URI, echo=DB_ECHO)


def make_session_class(engine: AsyncEngine) -> type[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False)


async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def main():
    root = sys.argv[-1]
    engine = get_engine()
    session_klass = make_session_class(engine)

    await create_tables(engine)

    async with session_klass() as session:
        logger.info("Creating CVEs")

        cve_data_processor = CveDataProcessor(session=session, directory_root=root)
        await cve_data_processor.run()

        await session.flush()
        await session.commit()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
