from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON
from services.vocabulary_handling import ru_eng, eng_ru
import random


# answers = random.sample(list(ru_eng.keys()), 4)
# print('answers = ', answers)
# question = random.choice(answers)
# print('question=', ru_eng.get(question))


def create_question_answers_keyboard() -> tuple:
    # Выбираем случайным образом 4 слова answers
    answers = random.sample(list(eng_ru.keys()), 4)
    # Формируем список переводов answers_question
    answers_question = [eng_ru[i] for i in answers]
    # print(answers_question)
    # Из answers назначаем вопрос
    question = random.choice(answers)
    # print('question=', question)
    answer_question = eng_ru[question]
    # print(answer_question)
    # Создаем объект клавиатуры
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    '''# Создаем кнопку-вопрос
    kb_builder.row(InlineKeyboardButton(text=f'{LEXICON["question_ru"]} {ru_eng.get(question)}'))'''
    # Наполняем клавиатуру кнопками-ответами
    for button in answers_question:
        kb_builder.row(InlineKeyboardButton(text=f'{button}', callback_data=str(button)))
    # kb_builder.adjust(10, repeat=True)
    return question, kb_builder.as_markup(), answer_question
    # возвращаем: вопрос, клавиатуру с вариантами ответов, правильный ответ


# create_question_answers_keyboard()
