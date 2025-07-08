import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import get_settings
from db.database import get_engine, get_session_maker, init_db
from utils.logger import logger
from handlers import register_handlers
from utils.db_middleware import DBSessionMiddleware
from utils.settings_middleware import SettingsMiddleware


async def main() -> None:
    settings = get_settings()
    engine = get_engine(settings.db_path)
    await init_db(engine)

    bot = Bot(settings.token, parse_mode='HTML')
    dp = Dispatcher(storage=MemoryStorage())

    session_maker = get_session_maker(engine)
    dp.message.middleware(DBSessionMiddleware(session_maker))
    dp.message.middleware(SettingsMiddleware(settings))

    register_handlers(dp)

    logger.info('Bot started')
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
