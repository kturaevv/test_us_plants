from typing import Any

from sqlalchemy import (
    CursorResult,
    Insert,
    MetaData,
    Select,
    Update,
)

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

from src.config import settings
from src.constants import DB_NAMING_CONVENTION

DATABASE_URL = str(settings.DATABASE_URL)

async_engine = create_async_engine(DATABASE_URL)
metadata = MetaData()


async def fetch_one(select_query: Select | Insert | Update) -> dict[str, Any] | None:
    async with async_engine.begin() as conn:
        cursor: CursorResult = await conn.execute(select_query)
        return cursor.first()._asdict() if cursor.rowcount > 0 else None


async def fetch_all(select_query: Select | Insert | Update) -> list[dict[str, Any]]:
    async with async_engine.begin() as conn:
        cursor: CursorResult = await conn.execute(select_query)
        return [r._asdict() for r in cursor.all()]

async def execute(select_query: Insert | Update) -> None:
    async with async_engine.begin() as conn:
        await conn.execute(select_query)


async def execute_raw(query: str) -> dict:
    async with async_engine.begin() as conn:
        cursor = await conn.execute(text(query))
        return [r._asdict() for r in cursor.all()]
