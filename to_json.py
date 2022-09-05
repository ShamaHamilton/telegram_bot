import json

curse_words = []

with open('curse_words.txt', encoding='utf-8') as read_file:
    for i in read_file:
        n = i.lower().split('\n')[0]
        if n != '':
            curse_words.append(n)

with open('cenz.json', 'w', encoding='utf-8') as e:
    json.dump(curse_words, e)
