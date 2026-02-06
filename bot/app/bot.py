import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.core.config import settings
from app.core.logging import setup_logging
from app.db.shared_sqlite import init_db
from app.handlers.gatekeeper import router as gatekeeper_router
from app.handlers.join_requests import router as join_router


def create_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()
    dispatcher.include_router(gatekeeper_router)
    dispatcher.include_router(join_router)
    return dispatcher


async def main() -> None:
    setup_logging()
    logger = logging.getLogger("bot")
    await init_db()

    bot = Bot(token=settings.bot_token)
    dispatcher = create_dispatcher()
    logger.info("Бот запущено")
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
