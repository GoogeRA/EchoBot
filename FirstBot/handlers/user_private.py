from aiogram import types, F, Router
from aiogram.filters import CommandStart, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards import authorized_user_kbds

user_private_router = Router()


class ShowIndex(StatesGroup):
    index_type = State()
    date = State()


@user_private_router.message(StateFilter(None), CommandStart())
async def start_cmd(message: types.message, state: FSMContext):
    await message.answer("Добро пожаловать! Это первая версия бота команды DevMinds. Для начала выберите показатель, "
                         "который хотите просмотреть.", reply_markup=authorized_user_kbds.start_kb)
    await state.set_state(ShowIndex.index_type)


# @user_private_router.message(ShowIndex.index_type, F.text == "Выручка")
# @user_private_router.message(ShowIndex.index_type, F.text == "Затраты")
@user_private_router.message(ShowIndex.index_type, or_f(F.text == "Прибыль", F.text == "Затраты", F.text == "Выручка"))
async def profit(message: types.message, state: FSMContext):
    await state.update_data(index_type=message.text)
    await message.answer("Показатель: " + message.text + "\nТеперь выберите временной промежуток",\
                         reply_markup=authorized_user_kbds.date_kb)
    await state.set_state(ShowIndex.date)


@user_private_router.message(ShowIndex.date, or_f(F.text == "Месяц", F.text == "Квартал", F.text == "Год"))
async def date(message: types.message, state: FSMContext):
    await state.update_data(date=message.text)
    data = await state.get_data()
    await message.answer(str(data), reply_markup=authorized_user_kbds.del_kb)
    await state.clear()




