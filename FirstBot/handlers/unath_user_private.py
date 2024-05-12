from aiogram import types, F, Router
from EchoBot.FirstBot.filters.authorized_filter import NotAuthorized

unath_user_router = Router()
unath_user_router.message.filter(NotAuthorized())


@unath_user_router.message()
async def answer(message: types.Message):
    await message.answer("Вы не авторизованы. Для авторизации обратитесь к администратору")