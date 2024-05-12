from aiogram.filters import Filter
from aiogram import types
from EchoBot.FirstBot.database.authorization import is_authorized


class IsAuthorized(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message):
        return is_authorized(message.from_user.id)


class NotAuthorized(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message):
        return not(is_authorized(message.from_user.id))


