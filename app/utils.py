import os
import sqlite3


def create_db() -> None:
    """
    To create a database.
    Для создания БД.
    """
    con = sqlite3.connect("engDB.db")
    cur = con.cursor()
    table_db: dict = {
        'verbs': ('eng_verb', 'rus_verb'),
        'nouns': ('eng_noun', 'rus_noun'),
        'adjectives': ('eng_adjective', 'rus_adjective'),
    }
    for key, value in table_db.items():
        column_eng, column_rus = value
        cur.execute(f'CREATE TABLE {key} ({column_eng} '
                    f'NOT NULL, {column_rus} NOT NULL)')
    con.close()


def connect_sql() -> None:
    """
    Checking for the presence of a database.
    Проверка на наличие БД.
    """
    if not os.path.exists("engDB.db"):
        create_db()
