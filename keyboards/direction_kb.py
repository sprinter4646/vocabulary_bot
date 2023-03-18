# модуль для формирования клавиатуры инлайн кнопок с направлениями перевода
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON


def create_direction_keyboard() -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Создаем кнопки eng_ru и ru_eng
    kb_builder.row(InlineKeyboardButton(text=f'{LEXICON["direction_eng_ru"]}', callback_data=str("direction_eng_ru")),
                   InlineKeyboardButton(text=f'{LEXICON["direction_ru_eng"]}', callback_data=str("direction_ru_eng")))
    # Возвращаем инлайн-клавиатуру
    return kb_builder.as_markup()
