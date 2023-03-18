# модуль для формирования кнопок с ответами
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON
from services.vocabulary_handling import ru_eng, eng_ru
import random


def create_question_answers_keyboard(direction) -> tuple:
    # определяем вид словаря в зависимости от direction
    slovar = (ru_eng if direction == 'direction_ru_eng' else eng_ru)
    # Выбираем случайным образом 4 слова answers
    answers = random.sample(list(slovar.keys()), 4)
    # Формируем список переводов answers_question
    answers_question = [slovar[i] for i in answers]
    # Из answers назначаем question
    question = random.choice(answers)
    # определяем answer_question ответ на question
    answer_question = slovar[question]
    # print(answer_question)
    # Создаем объект клавиатуры
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Наполняем клавиатуру кнопками-ответами
    for button in answers_question:
        kb_builder.row(InlineKeyboardButton(text=f'{button}', callback_data=str(button)))
    # возвращаем: вопрос, клавиатуру с вариантами ответов, правильный ответ
    return question, kb_builder.as_markup(), answer_question, answers_question
