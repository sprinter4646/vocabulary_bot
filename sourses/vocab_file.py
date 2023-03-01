# формирует словарь words из файла 2000full.txt
with open('2000full.txt') as file:
    words = {(row[:row.index('\t')]): row[row.index('\t')+1:row.index('\n')] for row in file}
    file.seek(0)
    for k, v in words.items():
        print(k, v)
    total_words = len([row for row in file])
    print('total_words=', total_words)


