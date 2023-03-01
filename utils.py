import sqlite3
import tkinter as tk
from write_or_read_db import read_db


def create_db() -> None:
    """Для создания БД."""
    con = sqlite3.connect("engDB.db")
    cur = con.cursor()
    table_db: dict = {
        'verbs': ('eng_verb', 'rus_verb'),
        'nouns': ('eng_noun', 'rus_noun'),
        'adjectives': ('eng_adjective', 'rus_adjective'),
    }
    for key, value in table_db.items():
        column_eng, column_rus = value
        cur.execute(f'CREATE TABLE {key} ({column_eng} NOT NULL, {column_rus} NOT NULL)')
    con.close()

bol_list: list = list()

    
		
    
    
