from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

del_kb = ReplyKeyboardRemove()

start_kb = ReplyKeyboardMarkup(
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

date_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Месяц"),
            KeyboardButton(text="Квартал"),
            KeyboardButton(text="Год"),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите промежуток"
)