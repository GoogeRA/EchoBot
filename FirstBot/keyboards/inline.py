import calendar

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
#from EchoBot.FirstBot.database.db import MetricTypes
from aiogram.utils.keyboard import InlineKeyboardBuilder


start_kb_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Посмотреть показатель', callback_data='Посмотреть показатель')
        ]
    ]
)

start_or_graph_kb_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Посмотреть показатель', callback_data='Посмотреть показатель'),
            InlineKeyboardButton(text='Создать график', callback_data='Создать график')
        ]
    ]
)


date_years_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="2022", callback_data="year_2022"),
            InlineKeyboardButton(text="2023", callback_data="year_2023"),
            InlineKeyboardButton(text="2024", callback_data="year_2024"),
        ]
    ]
)

months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
          'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
date_months_inline = InlineKeyboardBuilder()
for i in range(0,12):
    date_months_inline.add(InlineKeyboardButton(text=months[i], callback_data='month_'+str(i+1)))


def date_days_inline(month: int):
    year = 2024
    date_days_inline_kb = InlineKeyboardBuilder()
    weekday, days = calendar.monthrange(year, month)
    for i in range(weekday):
        date_days_inline_kb.add(InlineKeyboardButton(text='-', callback_data='day_None'))
    for i in range(1, days+1):
        date_days_inline_kb.add(InlineKeyboardButton(text=str(i), callback_data='day_'+str(i)))
    for i in range(35 - weekday - days):
        date_days_inline_kb.add(InlineKeyboardButton(text='-', callback_data='day_None'))
    return date_days_inline_kb.adjust(7, 7, 7, 7, 7).as_markup()


get_index_type_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Выручка", callback_data="Выручка"),
            InlineKeyboardButton(text="Затраты", callback_data="Затраты"),
            InlineKeyboardButton(text="Прибыль", callback_data="Прибыль"),
        ]
    ]
)

get_date_type_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="На конец месяца", callback_data="На конец месяца"),
            InlineKeyboardButton(text="На конец квартала", callback_data="На конец квартала")
        ],
        [
            InlineKeyboardButton(text="На конец года", callback_data="На конец года"),
            InlineKeyboardButton(text="На дату", callback_data="На дату"),
            InlineKeyboardButton(text="С даты на дату", callback_data="С даты на дату")
        ]
    ]
)

get_div_type_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Регион", callback_data="Регион"),
            InlineKeyboardButton(text="Проект", callback_data="Проект"),
            InlineKeyboardButton(text="Объект", callback_data="Объект")
        ]
    ]
)