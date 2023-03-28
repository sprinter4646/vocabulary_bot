# модуль для подготовки словарей из текстового файла
VOCABULARY_PATH = r'/home/oleg/Yandex.Disk/PYTHON_ubuntu/REPOS/vocabulary_bot/vocabulary/2000full.txt'

with open(VOCABULARY_PATH, 'r', encoding='utf-8') as file:
    eng_ru: dict[str, str] = {(row[:row.index('\t')]): row[row.index('\t') + 1:row.index('\n')] for row in file}
    ru_eng: dict[str, str] = dict(zip(eng_ru.values(), eng_ru.keys()))
