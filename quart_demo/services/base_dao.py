import typing
from typing import TypeVar

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase

from quart_demo.database.connection import async_session

T = TypeVar("T", bound=DeclarativeBase)


class BaseDao:
    @staticmethod
    async def get_all(model: typing.Type[T], *criteria: typing.Any, opt: typing.Any | None) -> list[T]:
        async with async_session.begin() as session:
            result = await session.execute(sa.select(model).filter(*criteria).options(opt))
            return typing.cast(list[T], result.scalars().all())

    @staticmethod
    async def get_one(model: typing.Type[T], *criteria: typing.Any) -> T:
        async with async_session.begin() as session:
            result = await session.execute(sa.select(model).filter(*criteria))
            return typing.cast(T, result.scalars().first())

    @staticmethod
    async def create(model: typing.Type[T], **kwargs: typing.Any) -> T:
        async with async_session.begin() as session:
            instance = model(**kwargs)
            session.add(instance)
            await session.commit()
            return instance

    @staticmethod
    async def update(model: typing.Type[T], *criteria: typing.Any, **kwargs: typing.Any) -> None:
        async with async_session.begin() as session:
            result = await session.execute(sa.update(model).filter(*criteria).values(**kwargs))

    @staticmethod
    async def delete(model: typing.Type[T], *criteria: typing.Any) -> int:
        async with async_session.begin() as session:
            result = await session.execute(sa.delete(model).filter(*criteria))
            await session.commit()
            return result.rowcount
