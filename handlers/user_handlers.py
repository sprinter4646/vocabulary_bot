from copy import deepcopy

from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import CallbackQuery, Message
from database.database import user_dict_template, users_db
from keyboards.direction_kb import create_direction_keyboard
from keyboards.answers_kb import create_question_answers_keyboard
from keyboards.further_kb import create_further_kb
from lexicon.lexicon import LEXICON
from services.vocabulary_handling import ru_eng, eng_ru

router: Router = Router()


# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
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


# Этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])


# Этот хэндлер будет срабатывать на команду "/begin"
# и отправлять пользователю клавиатуру с направлениями перевода
@router.message(Command(commands='begin'))
async def process_begin_command(message: Message):
    await message.answer(LEXICON['begin'], reply_markup=create_direction_keyboard())


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data 'direction_ru_eng' , 'direction_eng_ru' или 'next_word'
@router.callback_query(Text(text=['direction_ru_eng', 'direction_eng_ru', 'next_word']))
async def process_direction_press(callback: CallbackQuery):
    global answers_result, direction  # Делаем глобальными:
    # answers_result чтобы использовать в хэндлере проверки ответа check_answer
    # direction чтобы кнопка next_word формировала слово и клавиатуру с ответами используя ранее выбранное direction
    if callback.data == 'next_word':  # Если кнопка с next_word заново формируем слово-вопрос и клавиатуру с
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


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery с data 'cancel'
# и выводит статистику тренировки пользователю
@router.callback_query(Text(text='xxx'))
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=f'Тренировка словарного запаса английского языка завершена.'
             f'\nСтатистика тренировки: {users_db[callback.from_user.id]["correct_answers"]} верных ответов '
             f'из {users_db[callback.from_user.id]["questions"]} вопросов = {users_db[callback.from_user.id]["SCORE"]}')


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery с data 'текст кнопки' с вариантом перевода и сверять с
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


'''
# Этот хэндлер будет срабатывать на команду "/continue"
# и отправлять пользователю страницу книги, на которой пользователь
# остановился в процессе взаимодействия с ботом
@router.message(Command(commands='continue'))
async def process_continue_command(message: Message):
    text = book[users_db[message.from_user.id]['page']]
    await message.answer(
                text=text,
                reply_markup=create_pagination_keyboard(
                    'backward',
                    f'{users_db[message.from_user.id]["page"]}/{len(book)}',
                    'forward'))


# Этот хэндлер будет срабатывать на команду "/bookmarks"
# и отправлять пользователю список сохраненных закладок,
# если они есть или сообщение о том, что закладок нет
@router.message(Command(commands='bookmarks'))
async def process_bookmarks_command(message: Message):
    if users_db[message.from_user.id]["bookmarks"]:
        await message.answer(
            text=LEXICON[message.text],
            reply_markup=create_bookmarks_keyboard(
                *users_db[message.from_user.id]["bookmarks"]))
    else:
        await message.answer(text=LEXICON['no_bookmarks'])


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "вперед"
# во время взаимодействия пользователя с сообщением-книгой
@router.callback_query(Text(text='forward'))
async def process_forward_press(callback: CallbackQuery):
    if users_db[callback.from_user.id]['page'] < len(book):
        users_db[callback.from_user.id]['page'] += 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                    'backward',
                    f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                    'forward'))
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "назад"
# во время взаимодействия пользователя с сообщением-книгой
@router.callback_query(Text(text='backward'))
async def process_backward_press(callback: CallbackQuery):
    if users_db[callback.from_user.id]['page'] > 1:
        users_db[callback.from_user.id]['page'] -= 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
                text=text,
                reply_markup=create_pagination_keyboard(
                    'backward',
                    f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                    'forward'))
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с номером текущей страницы и добавлять текущую страницу в закладки
@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
async def process_page_press(callback: CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].add(
        users_db[callback.from_user.id]['page'])
    await callback.answer('Страница добавлена в закладки!')


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "редактировать" под списком закладок
@router.callback_query(Text(text='edit_bookmarks'))
async def process_edit_press(callback: CallbackQuery):
    await callback.message.edit_text(
                text=LEXICON[callback.data],
                reply_markup=create_edit_keyboard(
                                *users_db[callback.from_user.id]["bookmarks"]))
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "отменить" во время работы со списком закладок (просмотр и редактирование)
@router.callback_query(Text(text='cancel'))
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])
    await callback.answer()

'''
