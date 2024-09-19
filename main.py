import asyncio
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core import settings, db_helper
from api import router as api_router
from dependencies.broker_consumer import get_broker_consumer


@asynccontextmanager
async def lifespan(app: FastAPI):
    # async with db_helper.engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    #  startup
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] [%(asctime)s] %(name)s: %(message)s",
    )
    consumer = get_broker_consumer()
    print(1)
    asyncio.create_task(consumer.consume_callback_message())
    print(23)
    yield
    # shutdown
    # async with db_helper.engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    await db_helper.dispose()


main_app = FastAPI(
    lifespan=lifespan,
    # быстрее сериализация и десериализация
    default_response_class=ORJSONResponse,
)

main_app.include_router(
    router=api_router,
)

if __name__ == "__main__":
    uvicorn.run(
        app=settings.config.app,
        reload=settings.config.reload,
        host=settings.config.host,
        port=settings.config.port,
    )
