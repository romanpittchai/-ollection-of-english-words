import sqlite3
from write_or_read_db import write_db, read_db


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

def write_or_read_db() -> None:
	"""Выбор чтения или записи. Вызов соответствующей функции."""
	print('Write or read the database?') # !!! написать проверку на дурака
	w_or_r: str = input('w - 0, r - 1 ')
	if w_or_r == '0':
		write_db()
	elif w_or_r == '1':
		read_db()
	elif w_or_r == 'exit':
		quit()
	
