import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import CommandStart

bot = Bot(token='6801876089:AAFwcbtWvYW2LRKH0RzW2fLtbMVr_-4KUzk')

dp = Dispatcher()
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer('ПРИВЕТ')


@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())