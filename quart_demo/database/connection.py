from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from quart_demo.config import settings

engine = create_async_engine(settings.database.uri, echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False)
