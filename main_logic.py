import os
import sqlite3

from utils import create_db, write_or_read_db


def connect_sql():
    """Прверка на наличие БД. Создание, чтение или запись в БД."""
    if not os.path.exists("engDB.db"):
        create_db()
    #write_or_read_db()

    
#def main():
#    """Главная функция."""
#    connect_sql()


#if __name__ == "__main__":
#    main()
