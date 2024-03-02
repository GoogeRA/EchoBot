import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import CommandStart

from EchoBotRobertGooge.Config import TOKEN
bot = Bot(token=TOKEN)

dp = Dispatcher()
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать?!")
@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())