from aiogram import types, F, Router
from aiogram.filters import CommandStart, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards import authorized_user_kbds
#from database import db

user_private_router = Router()


class ShowIndex(StatesGroup):
    index_type = State()
    date_type = State()
    date = State()
    div_type = State()


@user_private_router.message(StateFilter(None), CommandStart())
async def start_cmd(message: types.message):
    await message.answer("Добро пожаловать! Это вторая версия бота команды DevMinds. Выберите действие",\
                         reply_markup=authorized_user_kbds.start_kb)


@user_private_router.message(StateFilter(None), F.text == "Посмотреть показатель")
async def show_index_cmd(message: types.message, state: FSMContext):
    await message.answer("Выберите показатель, который хотите просмотреть",\
                         reply_markup=authorized_user_kbds.get_index_type_kb)
    await state.set_state(ShowIndex.index_type)


@user_private_router.message(ShowIndex.index_type, or_f(F.text == "Прибыль", F.text == "Затраты", F.text == "Выручка"))
async def get_index_type(message: types.message, state: FSMContext):
    await state.update_data(index_type=message.text)
    await message.answer("Показатель: " + message.text + "\nВыберите временной промежуток",\
                         reply_markup=authorized_user_kbds.get_date_type_kb)
    await state.set_state(ShowIndex.date_type)


@user_private_router.message(ShowIndex.date_type, or_f(F.text == "На конец месяца", F.text == "На конец квартала",\
                                                  F.text == "На конец года", F.text == "На дату"))
async def get_date_type(message: types.message, state: FSMContext):
    await state.update_data(date_type=message.text)
    await message.answer("Временной срез: " + message.text)
    if message.text == "На дату":
        await state.set_state(ShowIndex.date)
    else:
        await state.update_data(date=None)
        await message.answer("Выберите тип среза", reply_markup=authorized_user_kbds.get_div_type_kb)
        await state.set_state(ShowIndex.div_type)


@user_private_router.message(ShowIndex.div_type, or_f(F.text == "Регион"))
async def get_div_type(message: types.message, state: FSMContext):
    await state.update_data(div_type=message.text)
    data = await state.get_data()
#    answer = db.get_data(data["index_type"], data["date_type"], data["div_type"], data["date"])
    await message.answer("data:   " + str(data))
#    await message.answer(answer)
    await message.answer("Выберите действие", reply_markup=authorized_user_kbds.start_kb)
    await state.clear()




