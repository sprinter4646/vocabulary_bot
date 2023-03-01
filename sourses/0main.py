# Работа бота в консоли компьютера без подключения к телеграм
import random
total_questions = int(input('Введите ОБЩЕЕ количество СЛОВ за раунд:'))

with open('2000full.txt') as file:
    vocabulary = {(row[:row.index('\t')]): row[row.index('\t') + 1:row.index('\n')] for row in file}
    words = dict(zip(vocabulary.values(), vocabulary.keys()))
wrong_answers = int(input('Введите возможное количество неверных ответов:'))
counter = 0
counter_wrong_answers = 0
counter_wright_answers = 0

while counter_wrong_answers < wrong_answers and counter < total_questions:
    print(f'Всего слов: {counter} Из них: верно: {counter_wright_answers} неверно: {counter_wrong_answers}')
    answers = random.sample(list(words.keys()), 4)
    question = random.choice(answers)
    print(f'What is the English for {question}?')
    counter += 1

    for i, answer in enumerate(answers):
        print(f'{i + 1} {words[answer]}')

    user_answer = int(input())
    correct_answer = words[question]

    if answers[user_answer - 1] == question:
        print('Correct answer')
        counter_wright_answers += 1
    else:
        print(f'Correct answer was {correct_answer}')
        counter_wrong_answers += 1

print('GAME OVER')
print(f'TOTAL RESULT: Всего слов: {counter} Из них: верно: {counter_wright_answers} неверно: {counter_wrong_answers}')
print('YOUR SCORE = ', counter_wright_answers/counter)

