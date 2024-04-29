from aiogram import types, F, Router
from aiogram.filters import CommandStart, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from EchoBot.FirstBot.database import db
from EchoBot.FirstBot.keyboards.inline import start_kb_inline, get_index_type_inline, get_date_type_inline, get_div_type_inline, \
    date_months_inline, date_days_inline, date_years_inline
import EchoBot.FirstBot.handlers.case_mapping as case_mapping
from datetime import date
from typing import  Type

user_private_router = Router()


class ShowIndex(StatesGroup):
    index_type = State()
    date_type = State()
    date = State()
    div_type = State()


async def send_metric_data(message: types.Message, metric_types: list, request: dict):
    result = case_mapping.generate_result_string(request)
    await message.answer("Данные по запросу: " + result, reply_markup=None)

    for metric_type in metric_types:
        answer = db.get_data(metric_type, request["index_type"], request["date_type"], request["div_type"],
                             request["date"], request["date_stop"]).all()
        await message.answer(case_mapping.metric_mapping(metric_type))

        for item in answer:
            await message.answer(
                f"Значение: {item[0]}\nНа дату: {item[1].strftime('%d-%m-%Y')}\nЗаписан: {item[2].strftime('%d-%m-%Y')}")

@user_private_router.message(StateFilter(None), CommandStart())
async def start_cmd(message: types.message):
    await message.answer("Добро пожаловать! Это вторая версия бота команды DevMinds. Выберите действие",
                         reply_markup=start_kb_inline)


# @user_private_router.message(StateFilter(None), F.text == "Посмотреть показатель")
# async def show_index_cmd(message: types.message, state: FSMContext):
#     await message.answer("Выберите показатель, который хотите просмотреть", \
#                          reply_markup=authorized_user_kbds.get_index_type_kb)
#     await state.set_state(ShowIndex.index_type)


# @user_private_router.message(ShowIndex.index_type, or_f(F.text == "Прибыль", F.text == "Затраты", F.text == "Выручка"))
# async def get_index_type(message: types.message, state: FSMContext):
#     await state.update_data(index_type=message.text)
#     await message.answer("Показатель: " + message.text + "\nВыберите временной промежуток", \
#                          reply_markup=authorized_user_kbds.get_date_type_kb)
#     await state.set_state(ShowIndex.date_type)


# @user_private_router.message(ShowIndex.date_type, or_f(F.text == "На конец месяца", F.text == "На конец квартала", \
#                                                        F.text == "На конец года", F.text == "На дату"))
# async def get_date_type(message: types.message, state: FSMContext):
#     await state.update_data(date_type=message.text)
#     await message.answer("Временной срез: " + message.text)
#     if message.text == "На дату":
#         await state.set_state(ShowIndex.date)
#     else:
#         await state.update_data(date=None)
#         await message.answer("Выберите тип среза", reply_markup=authorized_user_kbds.get_div_type_kb)
#         await state.set_state(ShowIndex.div_type)


# @user_private_router.message(ShowIndex.div_type, or_f(F.text == "Регион"))
# async def get_div_type(message: types.message, state: FSMContext):
#     await state.update_data(div_type=message.text)
#     data = await state.get_data()
#     #    answer = db.get_data(data["index_type"], data["date_type"], data["div_type"], data["date"])
#     await message.answer("data:   " + str(data))
#     #    await message.answer(answer)
#     await message.answer("Выберите действие", reply_markup=authorized_user_kbds.start_kb)
#     await state.clear()

# THIS IS START OF GETTING DATA
@user_private_router.callback_query(F.data == "Посмотреть показатель")
async def show_index_cmd(callback: types.CallbackQuery, state: FSMContext):
    # await callback.message.answer("Выберите показатель, который хотите просмотреть",\
    #                      reply_markup=authorized_user_kbds.get_index_type_kb)
    await callback.message.edit_text(text="Выберите показатель, который хотите просмотреть",
                                     reply_markup=get_index_type_inline)
    await state.set_state(ShowIndex.index_type)
    await callback.answer()


# TYPE OF DATA
@user_private_router.callback_query(ShowIndex.index_type,
                                    or_f(F.data == 'Выручка', F.data == 'Прибыль', F.data == 'Затраты'))
async def get_index_type_cmd(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(index_type=callback.data)
    await callback.message.edit_text(text="Показатель: " + callback.data + "\nВыберите временной промежуток",
                                     reply_markup=get_date_type_inline)
    await state.set_state(ShowIndex.date_type)


# DATE
@user_private_router.callback_query(ShowIndex.date_type,
                                    or_f(F.data == "На конец месяца", F.data == "На конец квартала",
                                         F.data == "На конец года", F.data == "На дату"))
async def det_date_type_cmd(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(date_type=callback.data)
    if callback.data == "На дату":
        await callback.message.edit_text(text="Выберите год",
                                         reply_markup=date_years_inline)
        await state.set_state(ShowIndex.date)
    else:
        await state.update_data(date=None)
        await state.update_data(date_stop=None)
        await callback.message.edit_text(text="Выберите тип среза", reply_markup=get_div_type_inline)
        await state.set_state(ShowIndex.div_type)


@user_private_router.callback_query(ShowIndex.date, F.data.startswith('year_'))
async def get_year_cmd(callback: types.CallbackQuery, state: FSMContext):
    year = int(callback.data.split('_')[-1])
    await state.update_data(date=date(year, 1, 1))
    await callback.message.edit_text(text="Выберите месяц",
                                     reply_markup=date_months_inline.adjust(3, 3, 3, 3).as_markup())


@user_private_router.callback_query(ShowIndex.date, F.data.startswith('month_'))
async def get_month_cmd(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    year = data["date"].year
    month = int(callback.data.split('_')[-1])
    await state.update_data(date=date(year, month, 1))
    await callback.message.edit_text(text="Выберите день",
                                     reply_markup=date_days_inline(month))


@user_private_router.callback_query(ShowIndex.date, F.data.startswith('day_'))
async def get_month_cmd(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    year = data["date"].year
    month = data["date"].month
    day_str = callback.data.split('_')[-1]
    if day_str != 'None':
        day = int(day_str)
        await state.update_data(date=date(year, month, day))
        await callback.message.edit_text(text="Выберите тип среза", reply_markup=get_div_type_inline)
        await state.set_state(ShowIndex.div_type)
    else:
        return


@user_private_router.callback_query(ShowIndex.div_type,
                                    or_f(F.data == "Регион", F.data == "Проект", F.data == "Объект"))
async def get_div_type_cmd(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(div_type=callback.data)
    request_data = await state.get_data()

    metric_types = [db.MetricTypes.MetricFact, db.MetricTypes.MetricPlan, db.MetricTypes.MetricPredict]
    await send_metric_data(callback.message, metric_types, request_data)

    await callback.message.answer("Выберите действие", reply_markup=start_kb_inline)
    await state.clear()
