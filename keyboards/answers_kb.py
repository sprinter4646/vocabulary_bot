from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON
from services.vocabulary_handling import eng_ru, ru_eng


def create_bookmarks_keyboard(*args: int) -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Наполняем клавиатуру кнопками-закладками в порядке возрастания
    for button in sorted(args):
        kb_builder.row(InlineKeyboardButton(
            text=f'{button} - {book[button][:100]}',
            callback_data=str(button)))
    # Добавляем в клавиатуру в конце две кнопки "Редактировать" и "Отменить"
    kb_builder.row(InlineKeyboardButton(
                        text=LEXICON['edit_bookmarks_button'],
                        callback_data='edit_bookmarks'),
                   InlineKeyboardButton(
                        text=LEXICON['cancel'],
                        callback_data='cancel'),
                   width=2)
    return kb_builder.as_markup()