import asyncio
import logging
from config import bot, dp, database
from handlers import daivinchi_router, start_router, view_router

async def main():
    # database.create_tables()
    dp.include_router(daivinchi_router)
    dp.include_router(start_router)
    dp.include_router(view_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
