# формирует словари (англ-русс и русс-англ) words и vocabulary из файла 2000full.txt
with open('2000full.txt') as file:
    vocabulary = {(row[:row.index('\t')]): row[row.index('\t')+1:row.index('\n')] for row in file}
    words = dict(zip(vocabulary.values(), vocabulary.keys()))
    print(words)

#     file.seek(0)
#     for k, v in words.items():
#         print(k, v)
#     total_words = len([row for row in file])
#     print('total_words=', total_words)

d = {"a": 1, "b": 2, "c": 3}
print(d)
print('1 VARIANT')
inverse_dic1 = {}
for key, val in d.items():
    inverse_dic1[val] = key
print(inverse_dic1)
print('2 VARIANT')
# dict_list = {"a": 1, "b": 2, "c": 3}
# inverse_dict2 = dict([val, key] for key, val in dict_list.items())
# print(inverse_dic2)
print('3 VARIANT')
dict_list = {"a": 1, "b": 2, "c": 3}
mydict_new = dict(zip(dict_list.values(), dict_list.keys()))
print(mydict_new)
