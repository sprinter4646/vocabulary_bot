from copy import deepcopy

from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import CallbackQuery, Message
from database.database import user_dict_template, users_db
from keyboards.direction_kb import create_direction_keyboard
from keyboards.answers_kb import create_question_answers_keyboard
from keyboards.further_kb import create_further_kb
from lexicon.lexicon import LEXICON

router: Router = Router()
# Делаем глобальными:
# answers_result, чтобы использовать в хэндлере проверки ответа check_answer
# direction чтобы кнопка next_word формировала слово и клавиатуру с ответами используя ранее выбранное direction
global answers_result, direction


# хэндлер на команду "/start" - # добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text])
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)
    # Наполняем базу данных для нового user.id нулевыми значениями
    users_db[message.from_user.id]['correct_answers'] = 0
    users_db[message.from_user.id]['questions'] = 0
    users_db[message.from_user.id]['SCORE'] = 0.0


# хэндлер на команду "/help" и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])


# хэндлер на команду "/direction" = отправляет пользователю клавиатуру с направлениями перевода
@router.message(Command(commands='direction'))
async def process_direction_command(message: Message):
    await message.answer(LEXICON['direction'], reply_markup=create_direction_keyboard())


# хэндлер на кнопку Завершить
@router.callback_query(Text(text='stop'))
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=f'{LEXICON["cancel_press"]} \n{LEXICON["score_press"]} '
                                          f'{users_db[callback.from_user.id]["correct_answers"]} '
                                          f'верных ответов из {users_db[callback.from_user.id]["questions"]} вопросов ='
                                          f' {users_db[callback.from_user.id]["SCORE"]}')


# хэндлер на апдейт типа CallbackQuery с data 'direction_ru_eng' , 'direction_eng_ru' или 'next_word'
@router.callback_query(Text(text=['direction_ru_eng', 'direction_eng_ru', 'next_word']))
async def process_direction_press(callback: CallbackQuery):
    global answers_result, direction
    if callback.data == 'next_word':  # Если поступает кнопка с next_word заново формируем слово-вопрос и клавиатуру с
        # вариантами ответа, используя ранее определенное пользователем direction
        answers_result = create_question_answers_keyboard(direction)
        reply_markup = answers_result[1]
        question = answers_result[0]
    else:  # Переопределяем direction и заново формируем слово-вопрос и клавиатуру с вариантами ответа
        direction = callback.data
        answers_result = create_question_answers_keyboard(callback.data)
        reply_markup = answers_result[1]
        question = answers_result[0]
    await callback.message.edit_text(
        text=f'Перевод для \n{question}:',
        reply_markup=reply_markup)


# хэндлер на апдейт типа CallbackQuery с data 'текст кнопки' с вариантом перевода и сверять с
# правильным ответом, изменяя users_db и выводя из нее статистику пользователю
@router.callback_query(Text)
async def check_answer(callback: CallbackQuery):
    reply_markup = create_further_kb()
    if callback.data == answers_result[2]:
        result = 'Верно'
        users_db[callback.from_user.id]['correct_answers'] += 1
    else:
        result = 'Неверно'

    users_db[callback.from_user.id]['questions'] += 1
    users_db[callback.from_user.id]['SCORE'] = users_db[callback.from_user.id]['correct_answers'] / \
                                               users_db[callback.from_user.id]['questions']
    await callback.message.edit_text(
        text=f'{result}\n Ваш ответ:      {answers_result[0]} - {callback.data} '
             f'\nВерный ответ: {answers_result[0]} - {answers_result[2]}'
             f'\nСтатистика тренировки: {users_db[callback.from_user.id]["correct_answers"]} верных ответов '
             f'из {users_db[callback.from_user.id]["questions"]} вопросов = {users_db[callback.from_user.id]["SCORE"]}',
        reply_markup=reply_markup)


# хэндлер на команду в меню '/score': 'Показать статистику' - отправляет пользователю статистику тренировки
@router.message(Command(commands='score'))
async def process_score_command(message: Message):
    await message.answer(text=f'\n{LEXICON["score_press"]} {users_db[message.from_user.id]["correct_answers"]} '
                              f'верных ответов из {users_db[message.from_user.id]["questions"]} вопросов = '
                              f'{users_db[message.from_user.id]["SCORE"]}')
