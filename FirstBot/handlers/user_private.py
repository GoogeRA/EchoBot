from aiogram import types, F, Router
from aiogram.filters import CommandStart, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
# from database import db
from keyboards.inline import start_kb_inline, get_index_type_inline, get_date_type_inline, get_div_type_inline, \
    date_months_inline, date_days_inline, date_years_inline
import handlers.case_mapping as case_mapping
from datetime import date

user_private_router = Router()


class ShowIndex(StatesGroup):
    index_type = State()
    date_type = State()
    date = State()
    div_type = State()


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
    data = await state.get_data()
    await callback.message.edit_text(str(data))
    await callback.message.answer("Выберите действие", reply_markup=start_kb_inline)
    await state.clear()

# OUTPUT VITALIK'S STUFF
# @user_private_router.callback_query(ShowIndex.div_type,
#                                     or_f(F.data == "Регион", F.data == "Проект", F.data == "Объект"))
# async def get_div_type_cmd(callback: types.CallbackQuery, state: FSMContext):
#     await state.update_data(div_type=callback.data)
#     request = await state.get_data()
#     result = case_mapping.generate_result_string(request)
#     answerFact = db.get_data(db.MetricTypes.MetricFact, request["index_type"], request["date_type"], request["div_type"], request["date"], request["date_stop"]).all()
#     answerPlan = db.get_data(db.MetricTypes.MetricPlan, request["index_type"], request["date_type"], request["div_type"], request["date"], request["date_stop"]).all()
#     answerPredict = db.get_data(db.MetricTypes.MetricPredict, request["index_type"], request["date_type"], request["div_type"], request["date"], request["date_stop"]).all()
#     await callback.message.edit_text("Данные по запросу:   " + result, reply_markup=None)
#     await callback.message.answer("Фактические значения показателя: " )
#     for i in range(len(answerFact)):
#         await   callback.message.answer("Значение: " + str(answerFact[i][0]) +
#                                         "\nНа дату: " + answerFact[i][1].strftime('%d-%m-%Y') +
#                                         "\nЗаписан: " + answerFact[i][2].strftime('%d-%m-%Y'))
#
#     await callback.message.answer("Плановые значения показателя: " )
#     for i in range(len(answerPlan)):
#         await   callback.message.answer("Значение: " + str(answerPlan[i][0]) +
#                                         "\nНа дату: " + answerPlan[i][1].strftime('%d-%m-%Y') +
#                                         "\nЗаписан: " + answerPlan[i][2].strftime('%d-%m-%Y'))
#
#     await callback.message.answer("Прогнозные значения показателя: " )
#     for i in range(len(answerPredict)):
#         await   callback.message.answer("Значение: " + str(answerPredict[i][0]) +
#                                         "\nНа дату: " + answerPredict[i][1].strftime('%d-%m-%Y') +
#                                         "\nЗаписан: " + answerPredict[i][2].strftime('%d-%m-%Y'))
#
#     await callback.message.answer("Выберите действие", reply_markup=start_kb_inline)
#     await state.clear()
