import sqlite3
from random import randint

# generate_joke
joke_cursor = sqlite3.connect("data/jokes.db").cursor()
joke_list = []


def get_joke():
    if len(joke_list):
        res = joke_list[-1]
        joke_list.pop()
        return res
    else:
        for i in range(100):
            ID = randint(1, 17077)  # range id
            text = joke_cursor.execute(f"SELECT text FROM jokes WHERE id='{ID}'").fetchall()[0][0]
            joke_list.append(text)
        return get_joke()
