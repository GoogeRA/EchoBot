from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

del_kb = ReplyKeyboardRemove()

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Посмотреть показатель")
        ]
    ],
    resize_keyboard=True
)
get_index_type_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Выручка"),
            KeyboardButton(text="Затраты"),
            KeyboardButton(text="Прибыль"),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите показатель"
)

get_date_type_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="На конец месяца"),
            KeyboardButton(text="На конец квартала"),
            KeyboardButton(text="На конец года"),
        ],
        [

            KeyboardButton(text="На дату"),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите промежуток"
)

get_div_type_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Регион")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите тип среза"
)