from asyncio import get_event_loop, new_event_loop

from aiogram import Bot, Dispatcher

from handlers import start
from handlers.menu import menu_handlers

from dotenv import load_dotenv

import logging


logging.basicConfig(
    format='[%(asctime)s] - [%(levelname)s] - [%(message)s]',
    level=logging.ERROR,
)


def on_startup():
    from db.db_interval import create_table, delay_post_table

    create_table()
    delay_post_table()


async def main():
    """
    Main function to start telegram bot

    :return: None
    """

    load_dotenv()

    on_startup()

    from config import TOKEN

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_routers(start.router, menu_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    loop = get_event_loop() or new_event_loop()

    loop.run_until_complete(
        loop.create_task(main()),
    )
