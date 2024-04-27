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

# start_kb_inline = InlineKeyboardBuilder()
# start_kb_inline.add(InlineKeyboardButton(text='Посмотреть показатель', callback_data='Посмотреть показатель'))

# get_metric_type_inline = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text="Фактический", callback_data="metricFact"),
#             InlineKeyboardButton(text="Плановый", callback_data="metricPlan"),
#             InlineKeyboardButton(text="Прогнозовый", callback_data="metricPredict"),
#         ]
#     ]
# )

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
            InlineKeyboardButton(text="На дату", callback_data="На дату")
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