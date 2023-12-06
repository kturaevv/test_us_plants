from contextlib import asynccontextmanager
from typing import AsyncGenerator

import redis.asyncio as aioredis
import sentry_sdk
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src import redis
from src.auth.router import router as auth_router
from src.config import app_configs, settings
from src.plants.router import router as plants_router


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    # Startup
    pool = aioredis.ConnectionPool.from_url(
        str(settings.REDIS_URL), max_connections=10, decode_responses=True
    )
    redis.redis_client = aioredis.Redis(connection_pool=pool)

    yield

    if settings.ENVIRONMENT.is_testing:
        return
    # Shutdown
    await pool.disconnect()


app = FastAPI(**app_configs, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE"),
    allow_headers=settings.CORS_HEADERS,
)

if settings.ENVIRONMENT.is_deployed:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
    )

from fastapi.openapi.utils import get_openapi

@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(plants_router, prefix="/plants", tags=["Plants"])
