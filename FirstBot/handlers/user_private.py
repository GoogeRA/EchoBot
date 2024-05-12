from aiogram import types, F, Router
from aiogram.filters import CommandStart, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from EchoBot.FirstBot.database import db
from EchoBot.FirstBot.keyboards.inline import start_kb_inline, get_index_type_inline, get_date_type_inline, get_div_type_inline, \
    date_months_inline, date_days_inline, date_years_inline, start_or_graph_kb_inline
import EchoBot.FirstBot.handlers.case_mapping as case_mapping
from datetime import date
from EchoBot.FirstBot.handlers.graph_handler import  create_graph, test_graph
from aiogram.types import  BufferedInputFile


user_private_router = Router()


class ShowIndex(StatesGroup):
    index_type = State()
    date_type = State()
    date = State()
    div_type = State()
    graph = State()



async def send_metric_data(message: types.Message, metric_types: list, request: dict):
    result = case_mapping.generate_result_string(request)
    await message.edit_text("Данные по запросу: " + result, reply_markup=None)

    metric_data = []


    for metric_type in metric_types:
        answer = db.get_data(metric_type, request["index_type"], request["date_type"], request["div_type"],
                             request["date"], request["date_stop"]).all()

        metric_data.append(answer)
        await message.answer(case_mapping.metric_mapping(metric_type))

        for item in answer:
            await message.answer(
                f"Значение: {item[0]}\nНа дату: {item[1].strftime('%d-%m-%Y')}"
                f"\nЗаписан: {item[2].strftime('%d-%m-%Y')}")

    return metric_data


@user_private_router.message(StateFilter(None), CommandStart())
async def start_cmd(message: types.message):
    await message.answer("Добро пожаловать! Это вторая версия бота команды DevMinds. Выберите действие",
                         reply_markup=start_kb_inline)


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
                                         F.data == "На конец года", F.data == "На дату", F.data == "С даты на дату"))
async def det_date_type_cmd(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(date_type=callback.data)
    if callback.data == "На дату":
        await state.update_data(date_stop=None)
        await callback.message.edit_text(text="Выберите год",
                                         reply_markup=date_years_inline)
        await state.update_data(date_state='One')
        await state.set_state(ShowIndex.date)
    elif callback.data == "С даты на дату":
        await callback.message.edit_text(text="Выберите год",
                                         reply_markup=date_years_inline)
        await state.update_data(date_type='На дату')
        await state.update_data(date_state=['Range', 'Not set'])
        await state.set_state(ShowIndex.date)
    else:
        await state.update_data(date=None)
        await state.update_data(date_stop=None)
        await callback.message.edit_text(text="Выберите тип среза", reply_markup=get_div_type_inline)
        await state.set_state(ShowIndex.div_type)


@user_private_router.callback_query(ShowIndex.date, F.data.startswith('year_'))
async def get_year_cmd(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    date_state = data.get('date_state')

    if date_state == 'One':
        year = int(callback.data.split('_')[-1])
        await state.update_data(date=date(year, 1, 1))
        await callback.message.edit_text(text="Выберите месяц",
                                         reply_markup=date_months_inline.adjust(3, 3, 3, 3).as_markup())
    elif date_state == ['Range', 'Not set']:
        year = int(callback.data.split('_')[-1])
        await state.update_data(date=date(year, 1, 1))
        await callback.message.edit_text(text="Выберите месяц",
                                         reply_markup=date_months_inline.adjust(3, 3, 3, 3).as_markup())
    elif date_state == ['Range', 'Set']:
        year = int(callback.data.split('_')[-1])
        await state.update_data(date_stop=date(year, 1, 1))
        await callback.message.edit_text(text="Выберите месяц",
                                         reply_markup=date_months_inline.adjust(3, 3, 3, 3).as_markup())



@user_private_router.callback_query(ShowIndex.date, F.data.startswith('month_'))
async def get_month_cmd(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    date_state = data.get('date_state')
    if date_state == 'One':
        year = data["date"].year
        month = int(callback.data.split('_')[-1])
        await state.update_data(date=date(year, month, 1))
        await callback.message.edit_text(text="Выберите день",
                                         reply_markup=date_days_inline(month))
    elif date_state == ['Range', 'Not set']:
        year = data["date"].year
        month = int(callback.data.split('_')[-1])
        await state.update_data(date=date(year, month, 1))
        await callback.message.edit_text(text="Выберите день",
                                         reply_markup=date_days_inline(month))
    elif date_state == ['Range', 'Set']:
        year = data["date_stop"].year
        month = int(callback.data.split('_')[-1])
        await state.update_data(date_stop=date(year, month, 1))
        await callback.message.edit_text(text="Выберите день",
                                         reply_markup=date_days_inline(month))


@user_private_router.callback_query(ShowIndex.date, F.data.startswith('day_'))
async def get_month_cmd(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    date_state = data.get('date_state')

    if date_state == 'One':
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
    elif date_state == ['Range', 'Not set']:
        year = data["date"].year
        month = data["date"].month
        day_str = callback.data.split('_')[-1]
        if day_str != 'None':
            day = int(day_str)
            await state.update_data(date=date(year, month, day))
            await state.update_data(date_state=['Range', 'Set'])
            await callback.message.edit_text(text="Выберите конечную дату", reply_markup=date_years_inline)
            await state.set_state(ShowIndex.date)
        else:
            return
    elif date_state == ['Range', 'Set']:
        year = data["date_stop"].year
        month = data["date_stop"].month
        day_str = callback.data.split('_')[-1]
        if day_str != 'None':
            day = int(day_str)
            await state.update_data(date_stop=date(year, month, day))
            await callback.message.edit_text(text="Выберите тип среза", reply_markup=get_div_type_inline)
            await state.set_state(ShowIndex.div_type)




@user_private_router.callback_query(ShowIndex.div_type,
                                    or_f(F.data == "Регион", F.data == "Проект", F.data == "Объект"))
async def get_div_type_cmd(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(div_type=callback.data)
    request_data = await state.get_data()

    metric_types = [db.MetricTypes.MetricFact, db.MetricTypes.MetricPlan, db.MetricTypes.MetricPredict]
    result_data = await send_metric_data(callback.message, metric_types, request_data)
    await state.update_data(result_data=result_data)

    await callback.message.answer("Выберите действие", reply_markup=start_or_graph_kb_inline)
    await state.set_state(ShowIndex.graph)



@user_private_router.callback_query(ShowIndex.graph,
                                    or_f(F.data == "Посмотреть показатель", F.data == "Создать график"))
async def get_graph_cmd(callback: types.CallbackQuery, state: FSMContext):
    action_choice = callback.data

    await callback.message.delete()
    if action_choice == "Посмотреть показатель":
        await state.clear()
    elif action_choice == "Создать график":
        state_data = await state.get_data()
        metric_data = state_data.get('result_data')
        # img_buffer = test_graph()
        metric_data = [[i[:-1] for i in k] for k in metric_data]

        img_buffer = create_graph(metric_data)

        input_file = BufferedInputFile(img_buffer.getvalue(), filename='graph.py')
        await callback.bot.send_photo(callback.message.chat.id, photo=input_file)
        await state.clear()
        await callback.message.answer("Выберите действие", reply_markup=start_kb_inline)

        # await callback.message.answer(str(metric_data))
        # await callback.message.answer(str(state_data))



