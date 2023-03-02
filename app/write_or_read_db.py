import sqlite3
import random
from tkinter import filedialog, messagebox


def info_for_db():
    """
    To notify that a record is in the database.
    Для оповещения, что запись в базе данных.
    """
    title = "Service message"
    massage = "Recorded in the DB!"
    return messagebox.showinfo(title, massage)


def write_db_consol(value, list_data) -> None:
    """
    Recording from the adjective console.
    Запись из консоли прилагательного.
    """
    data: list = list()
    for list_value in list_data:
        tuple_value: tuple = tuple((list_value).split())
        if len(tuple_value) != 2:
            continue
        data.append(tuple_value)
    try:
        con = sqlite3.connect("engDB.db")
        cur = con.cursor()
        cur.executemany(f'INSERT INTO {value} values (?, ?)', data)
        con.commit()
        con.close()
    except sqlite3.Error as error:
        print(error)
    info_for_db()


def write_db_file(value) -> None:
    """
    Writing to the database from a txt file.
    Запись в БД из txt файла.
    """
    filetypes = (
        ('Text files', '.txt'),
        ('All files', '.*')
    )
    data: list = list()
    filepath_open = (filedialog.askopenfilename
                     (filetypes=filetypes, defaultextension=''))
    if filepath_open:
        file_text = open(filepath_open, "r")
        try:
            con = sqlite3.connect("engDB.db")
            cur = con.cursor()
        except sqlite3.Error as error:
            print(error)
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
        info_for_db()


cur_obj_rus: list = list()


def read_db() -> list:
    """
    Reading the database for English words.
    Чтение БД для английских слов.
    """
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
    word_list: list = list()
    ran: int = 0
    cur_obj_rus.clear()
    for key, value in count_wr_tab.items():
        if not value:
            continue
        ran = random.randint(1, value)
        cur.execute(f'SELECT * FROM {key} WHERE rowid = {ran}')
        cur_obj = cur.fetchall()
        cur_obj_rus.append(cur_obj[0])
        for v in cur_obj:
            word_list.append(v[0])
    return word_list


def read_db_for_rus() -> list:
    """
    Reading the database for Russian words.
    Чтение БД для русских слов.
    """
    word_list: list = list()
    for v in cur_obj_rus:
        word_list.append(v[1])
    cur_obj_rus.clear()
    return word_list
