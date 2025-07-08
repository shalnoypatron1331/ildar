import asyncio
from aiogram import Bot, Dispatcher

from config import get_settings
from db.database import get_engine, get_session_maker, init_db
from utils.logger import logger
from handlers import setup as setup_handlers


async def main() -> None:
    settings = get_settings()
    engine = get_engine(settings.db_path)
    await init_db(engine)

    bot = Bot(settings.token, parse_mode='HTML')
    dp = Dispatcher()

    session_maker = get_session_maker(engine)
    setup_handlers(dp, session_maker)

    logger.info('Bot started')
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
