import asyncio
import os

from aiogram import Bot, Dispatcher, types
from handlers.user_private import user_private_router
from handlers.unath_user_private import unath_user_router
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()

dp.include_router(user_private_router)
dp.include_router(unath_user_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    # await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())