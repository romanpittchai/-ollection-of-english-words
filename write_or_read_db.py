import sqlite3
import random
import os
from tkinter import filedialog



def write_db_consol(value) -> None:
    """Запись из консоли прилагательного."""
    data: list = list()
    print('Вводите сначало английское слово,'
          ' потом русское слово через пробел и'
          ' и жмите Ввод. Для выхода введите ##')
    while True:
        word_for_db: str = input('-> ') # проверку на кол-во сделать и лишние знаки
        if word_for_db != '##':
            word_for_db = tuple(word_for_db.split())
            data.append(word_for_db)
        else:
            break
    con = sqlite3.connect("engDB.db")
    cur = con.cursor()
    cur.executemany(f'INSERT INTO {value} values (?, ?)', data)
    con.commit()
    con.close()
        

def write_db_file(value):   
    """Запись в БД из txt файла."""
    filetypes = (
        ('Text files', '.txt'),
        ('All files', '.*')
    )
    data: list = list()
    list_for_txt: list = list()
    con = sqlite3.connect("engDB.db")
    cur = con.cursor()
    try:
        filepath_open = (filedialog.askopenfilename
                         (filetypes=filetypes, defaultextension=''))
        if filepath_open:
            file_text = open(filepath_open, "r")
        while True:
            file_text_r: str = file_text.readline()
            if not file_text_r:
                break
            file_text_r = tuple(file_text_r.split())
            if len(file_text_r) != 2:
                continue
            data.append(file_text_r)
            list(file_text_r).clear()
            file_text_r = ''
        file_text.close()
        cur.executemany(f'INSERT INTO {value} values (?, ?)', data)
        con.commit()
        con.close()
    except (FileNotFoundError, IsADirectoryError) as error:
        print(f'There is no such file or directory! {error}')
        


def write_db() -> None:
    """Выбор источника записи."""
    print('Выберите источник данных.')
    cons_or_txt: str = input('consol - 0, file(txt) - 1 ')
    adjectives: str = 'adjectives'
    verbs: str = 'verbs'
    nouns: str = 'nouns'
    if cons_or_txt == '0':
        w_db: str = input('Что это будет(прил(0), сущ(1), гл(2)) ')
        if w_db == '0':
            write_db_consol(adjectives)
        elif w_db == '1':
            write_db_consol(nouns)
        elif w_db == '2':
            write_db_consol(verbs)
    elif cons_or_txt == '1':
        w_db: str = input('Что это будет(прил(0), сущ(1), гл(2)) ')
        if w_db == '0':
            write_db_file(adjectives)
        elif w_db == '1':
            write_db_file(nouns)
        elif w_db == '2':
            write_db_file(verbs)
        
    
def read_db():
    """Чтение БД."""
    name_tab: list = list()
    count_wr_tab: dict = {}
    con = sqlite3.connect("engDB.db")
    cur = con.cursor()
    cur.execute('SELECT * FROM sqlite_master WHERE type = "table"')
    all_tab = cur.fetchall()
    for value in all_tab:
         name_tab.append(value[1])
    for value in name_tab:
        cur.execute(f'SELECT Count(*) FROM {value}')
        obj_count_tab = cur.fetchall()
        count_wr_tab[value] = obj_count_tab[0][0]
    print('+ если хотите eng.')
    print('- если хотите перевод(после того, как вызвали eng).')
    print('## если хотите закончить.')
    word_list: list = list()
    cur_obj_rus: list = list()
    while True:
        var: str = input('-> ')
        if var == '+':
            cur_obj_rus.clear()
            ran: int = 0
            for key, value in count_wr_tab.items():
                ran = random.randint(1, value)
                cur.execute(f'SELECT * FROM {key} WHERE rowid = {ran}')
                cur_obj = cur.fetchall()
                cur_obj_rus.append(cur_obj[0])
                for v in cur_obj:
                    word_list.append(v[0])
            print(*word_list)
            word_list.clear()
        elif var == '-': # Проверку на то что уже вызвали eng и выводили 1 раз перевод
            word_list.clear() # Проверка на дурака (другое слово)
            for v in cur_obj_rus:
                word_list.append(v[1])
            print(*word_list)
            word_list.clear()
            cur_obj_rus.clear()
        elif var == '##':
            break
