VOCABULARY_PATH = '../vocabulary/2000full.txt'


# Функция, формирующая словарь словари
'''def prepare_vocabularies(path: str) -> type:
    with open(path, 'r', encoding='utf-8') as file:
        eng_ru: dict[str, str] = {(row[:row.index('\t')]): row[row.index('\t') + 1:row.index('\n')] for row in file}
        ru_eng: dict[str, str] = dict(zip(eng_ru.values(), eng_ru.keys()))
        print(eng_ru)
        print(ru_eng)
        return eng_ru, ru_eng'''


# Вызов функции prepare_book для подготовки книги из текстового файла
# prepare_vocabularies(VOCABULARY_PATH)

with open(VOCABULARY_PATH, 'r', encoding='utf-8') as file:
    ru_eng: dict[str, str] = {(row[:row.index('\t')]): row[row.index('\t') + 1:row.index('\n')] for row in file}
    # ru_eng: dict[str, str] = dict(zip(ru_eng.values(), ru_eng.keys()))
    print(ru_eng)
    # print(eng_ru)
