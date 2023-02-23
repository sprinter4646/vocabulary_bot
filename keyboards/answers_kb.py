from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON
from services.vocabulary_handling import ru_eng
import random

# answers = random.sample(list(ru_eng.keys()), 4)
# print('answers = ', answers)
# question = random.choice(answers)
# print('question=', ru_eng.get(question))


def create_question_answers_keyboard() -> InlineKeyboardMarkup:
    # Выбираем случайным образом 4 ответа answers
    answers = random.sample(list(ru_eng.keys()), 4)
    # Из answers назначаем вопрос
    question = random.choice(answers)
    # Создаем объект клавиатуры
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Создаем кнопку-вопрос
    kb_builder.row(InlineKeyboardButton(text=f'{LEXICON["question_ru"]} {ru_eng.get(question)}'))
    # Наполняем клавиатуру кнопками-ответами
    for button in answers:
        kb_builder.row(InlineKeyboardButton(text=f'{button}', callback_data=str(button)))
    # kb_builder.adjust(10, repeat=True)
    return kb_builder.as_markup()
