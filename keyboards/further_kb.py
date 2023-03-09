from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON


def create_further_kb() -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Создаем кнопки
    kb_builder.row(InlineKeyboardButton(text=f'{LEXICON["next_word"]}', callback_data="next_word"))
    kb_builder.row(InlineKeyboardButton(text=f'{LEXICON["cancel"]}', callback_data="stop"))
    return kb_builder.as_markup()
