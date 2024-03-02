import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import CommandStart, Command




from Config import TOKEN
bot = Bot(token = TOKEN)

stopCommand = Command('stop')
reactionCommand = Command('reaction')

dp = Dispatcher()
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Helloo Hiii hellooo :3")

@dp.message(stopCommand)
async def cmd_stop(message: types.Message):
    await message.answer('ok')

@dp.message(reactionCommand)
async def cmd_reaction(message_reaction: types.Message):
    await message_reaction.react([types.ReactionTypeEmoji(emoji = '🥰')])
    

@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text + " ты лох кста")
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())