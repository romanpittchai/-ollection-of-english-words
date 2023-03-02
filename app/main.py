import tkinter as tk
from tkinter import (Frame, Menu, Text, Scrollbar,
                     filedialog, messagebox, Tk, BooleanVar)

from utils import connect_sql
from write_or_read_db import (write_db_file,
                              write_db_consol,
                              read_db,
                              read_db_for_rus)


class TextEditor(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.up_menu()

    def up_menu(self) -> None:
        """
        Basic widgets.
        Базовые виджеты.
        """
        self.master.title("SimplyApp")
        main_menu = Menu(self)
        self.master.config(menu=main_menu)
        file_menu = Menu(main_menu, tearoff=0)
        file_menu_correction = Menu(main_menu, tearoff=0)
        mouse_menu = Menu(main_menu, tearoff=0)
        file_menu.add_command(label="New file",
                              command=self.new_file,
                              accelerator="Ctrl+N")
        file_menu.add_command(label="Open file",
                              command=self.select_and_open_file,
                              accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Save",
                              command=self.save_file,
                              accelerator="Ctrl+S")
        file_menu.add_command(label="Save as",
                              command=self.save_as_file,
                              accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit",
                              command=self.exit_from_editor,
                              accelerator="Ctrl+Q")
        file_menu_correction.add_command(label="Cut",
                                         command=self.cut_text,
                                         accelerator="Ctrl+X")
        file_menu_correction.add_command(label="Copy",
                                         command=self.copy_text,
                                         accelerator="Ctrl+C")
        file_menu_correction.add_separator()
        file_menu_correction.add_command(label="Paste",
                                         command=self.paste_text,
                                         accelerator="Ctrl+V")
        file_menu_correction.add_command(label="Select text",
                                         command=self.select_text,
                                         accelerator="Ctrl+A")

        mouse_menu.add_command(label="Save", command=self.save_file)
        mouse_menu.add_command(label="Save as", command=self.save_as_file)
        mouse_menu.add_separator()
        mouse_menu.add_command(label="Select text", command=self.select_text)
        mouse_menu.add_command(label="Cut", command=self.cut_text)
        mouse_menu.add_command(label="Copy", command=self.copy_text)
        mouse_menu.add_command(label="Paste", command=self.paste_text)

        def mouse_popup(event) -> None:
            """
            The initializer is a mouse key.
            Инициализатор клавишь для мыши.
            """
            try:
                mouse_menu.tk_popup(event.x_root, event.y_root)
            finally:
                mouse_menu.grab_release()

        self.bind_all("<Button-3>", mouse_popup)

        main_menu.add_cascade(label="File", menu=file_menu)
        main_menu.add_cascade(label="Сorrection",
                              menu=file_menu_correction)

        txtFrame = Frame(self.master)
        txtFrame.pack(side="bottom", fill="both", expand=True)
        self.txt_notes = Text(master=txtFrame, wrap="word")
        scrollbar = Scrollbar(master=txtFrame,
                              command=self.txt_notes.yview)
        self.txt_notes['yscrollcommand'] = scrollbar.set
        scrollbar.pack(side="right", fill="y")
        self.txt_notes.pack(side="bottom", fill="both", expand=True)

        true_adj = BooleanVar()
        true_ver = BooleanVar()
        true_noun = BooleanVar()

        def write_db_from_file() -> None:
            """
            Calling a function to write
            to the database from a file.
            When selecting the checkbox.
            Вызов функции для записи в БД из файла.
            При выборе чекбокса.
            """
            bool_dict: dict = {'adjectives': true_adj.get(),
                               'verbs': true_ver.get(),
                               'nouns': true_noun.get()}
            keys: list = list(bool_dict.keys())
            if bool_dict['adjectives']:
                write_db_file(keys[0])
            elif bool_dict['verbs']:
                write_db_file(keys[1])
            else:
                write_db_file(keys[2])

        def write_db_from_consol() -> None:
            """
            Calling the write function to
            the database from application consoles.
            When selecting the checkbox.
            Вызов функции записи в БД из
            консоли приложения. При выборе чекбокса.
            """
            bool_dict: dict = {'adjectives': true_adj.get(),
                               'verbs': true_ver.get(),
                               'nouns': true_noun.get()}
            keys: list = list(bool_dict.keys())
            get_from_consol: str = self.txt_notes.get("1.0", "end-1c")
            list_data: list = get_from_consol.splitlines()
            if bool_dict['adjectives']:
                write_db_consol(keys[0], list_data)
            elif bool_dict['verbs']:
                write_db_consol(keys[1], list_data)
            else:
                write_db_consol(keys[2], list_data)

        def read_db_eng() -> None:
            """
            Reading from the database (English).
            Чтение из БД(английский).
            """
            list_from_bd: list = read_db()
            if len(list_from_bd) == 0:
                pass
            else:
                index_cursor = self.txt_notes.index('insert')
                self.txt_notes.insert(index_cursor, list_from_bd)
                index_cursor = self.txt_notes.index('insert')
                self.txt_notes.insert(index_cursor, '\n')

        def read_db_rus() -> None:
            """
            Reading from the database (Russian).
            If the function of reading English
            words from the database was called before.
            Чтение из БД(Русский).
            Если прежде вызвана функция чтения
            из БД английских слов.
            """
            list_from_bd: list = read_db_for_rus()
            if len(list_from_bd) == 0:
                pass
            else:
                index_cursor = self.txt_notes.index('insert')
                self.txt_notes.insert(index_cursor, list_from_bd)
                index_cursor = self.txt_notes.index('insert')
                self.txt_notes.insert(index_cursor, '\n')

        buttonFrame = Frame(self.master)
        buttonFrame.pack(fill=tk.Y, ipadx=5, ipady=5)
        self.btn_sub_1 = tk.Button(master=buttonFrame,
                                   text="Read BD(eng)",
                                   command=read_db_eng)
        self.btn_sub_1.pack(side=tk.RIGHT, ipadx=20)
        self.btn_sub_2 = tk.Button(master=buttonFrame,
                                   text="Read BD(rus)",
                                   command=read_db_rus)
        self.btn_sub_2.pack(side=tk.RIGHT, ipadx=20)
        self.btn_sub_3 = tk.Button(master=buttonFrame,
                                   text="Write BD(text)",
                                   command=write_db_from_consol)
        self.btn_sub_3.pack(side=tk.RIGHT, ipadx=20)
        self.btn_sub_4 = tk.Button(master=buttonFrame,
                                   text="Write BD(file)",
                                   command=write_db_from_file)
        self.btn_sub_4.pack(side=tk.RIGHT, ipadx=20)

        chBoxFrame = Frame(self.master)
        chBoxFrame.pack(fill=tk.Y)

        def ckbox_adjectives() -> None:
            """
            Selecting a checkbox with an adjective.
            Выбор чек-бокса с прилагательным.
            """
            true_or_false: bool = true_adj.get()
            if true_or_false:
                self.ck_box_2.configure(state=tk.DISABLED)
                self.ck_box_3.configure(state=tk.DISABLED)
                self.btn_sub_1.configure(state=tk.DISABLED)
                self.btn_sub_2.configure(state=tk.DISABLED)
                self.btn_sub_3.configure(state=tk.NORMAL)
                self.btn_sub_4.configure(state=tk.NORMAL)
                self.btn_sub_clear.configure(state=tk.DISABLED)
            else:
                self.ck_box_2.configure(state=tk.NORMAL)
                self.ck_box_3.configure(state=tk.NORMAL)
                self.btn_sub_1.configure(state=tk.NORMAL)
                self.btn_sub_2.configure(state=tk.NORMAL)
                self.btn_sub_3.configure(state=tk.DISABLED)
                self.btn_sub_4.configure(state=tk.DISABLED)
                self.btn_sub_clear.configure(state=tk.NORMAL)

        def ckbox_verbs() -> None:
            """
            Selecting a checkbox with a verb.
            Выбор чек-бокса с глаголом.
            """
            true_or_false: bool = true_ver.get()

            if true_or_false:
                self.ck_box_1.configure(state=tk.DISABLED)
                self.ck_box_3.configure(state=tk.DISABLED)
                self.btn_sub_1.configure(state=tk.DISABLED)
                self.btn_sub_2.configure(state=tk.DISABLED)
                self.btn_sub_3.configure(state=tk.NORMAL)
                self.btn_sub_4.configure(state=tk.NORMAL)
                self.btn_sub_clear.configure(state=tk.DISABLED)
            else:
                self.ck_box_1.configure(state=tk.NORMAL)
                self.ck_box_3.configure(state=tk.NORMAL)
                self.btn_sub_1.configure(state=tk.NORMAL)
                self.btn_sub_2.configure(state=tk.NORMAL)
                self.btn_sub_3.configure(state=tk.DISABLED)
                self.btn_sub_4.configure(state=tk.DISABLED)
                self.btn_sub_clear.configure(state=tk.NORMAL)

        def ckbox_nouns() -> None:
            """
            Selecting a checkbox with a noun.
            Выбор чек-бокса с существительным.
            """
            true_or_false: bool = true_noun.get()
            if true_or_false:
                self.ck_box_1.configure(state=tk.DISABLED)
                self.ck_box_2.configure(state=tk.DISABLED)
                self.btn_sub_1.configure(state=tk.DISABLED)
                self.btn_sub_2.configure(state=tk.DISABLED)
                self.btn_sub_3.configure(state=tk.NORMAL)
                self.btn_sub_4.configure(state=tk.NORMAL)
                self.btn_sub_clear.configure(state=tk.DISABLED)
            else:
                self.ck_box_1.configure(state=tk.NORMAL)
                self.ck_box_2.configure(state=tk.NORMAL)
                self.btn_sub_1.configure(state=tk.NORMAL)
                self.btn_sub_2.configure(state=tk.NORMAL)
                self.btn_sub_3.configure(state=tk.DISABLED)
                self.btn_sub_4.configure(state=tk.DISABLED)
                self.btn_sub_clear.configure(state=tk.NORMAL)

        self.ck_box_1 = tk.Checkbutton(master=chBoxFrame,
                                       text="adjectives",
                                       command=ckbox_adjectives,
                                       variable=true_adj)
        self.ck_box_1.pack(side=tk.RIGHT, ipadx=20)
        self.ck_box_2 = tk.Checkbutton(master=chBoxFrame,
                                       text="verbs",
                                       command=ckbox_verbs,
                                       variable=true_ver)
        self.ck_box_2.pack(side=tk.RIGHT, ipadx=20)
        self.ck_box_3 = tk.Checkbutton(master=chBoxFrame,
                                       text="nouns",
                                       command=ckbox_nouns,
                                       variable=true_noun)
        self.ck_box_3.pack(side=tk.RIGHT, ipadx=20)

        def check_chbox() -> None:
            """
            Locking buttons and checkboxes
            of the database entry.
            Блокировка кнопок и чек-боксов записи в БД.
            """
            bool_list: list = [true_adj.get(), true_ver.get(), true_noun.get()]
            if all([bool_list]):
                self.ck_box_1.configure(state=tk.NORMAL)
                self.ck_box_2.configure(state=tk.NORMAL)
                self.ck_box_3.configure(state=tk.NORMAL)
                self.btn_sub_1.configure(state=tk.NORMAL)
                self.btn_sub_2.configure(state=tk.NORMAL)
                self.btn_sub_3.configure(state=tk.DISABLED)
                self.btn_sub_4.configure(state=tk.DISABLED)
        check_chbox()

        def clear() -> None:
            """
            Clear the text field.
            Очистить текстовое поле.
            """
            self.txt_notes.delete("1.0", "end-1c")

        buttonFrameTwo = Frame(self.master)
        buttonFrameTwo.pack(fill=tk.Y, ipadx=5, ipady=5)
        self.btn_sub_clear = tk.Button(master=buttonFrameTwo,
                                       text="Clear",
                                       command=clear)
        self.btn_sub_clear.pack(side=tk.RIGHT, ipadx=20)

        def key_non_shift(event) -> None:
            """
            Initializer of some keys (see codes).
            Инициализатор некоторых клавишь(см. коды).
            """
            keys_code = {
                (79, 32): self.select_and_open_file,
                (78, 57): self.new_file,
                (83, 39): self.save_file,
                (65, 38): self.select_text,
                (81, 24): self.exit_from_editor,
            }
            for key_coder, key_func in keys_code.items():
                if event.keycode in key_coder:
                    key_func()

        self.bind_all("<Control-KeyPress>", key_non_shift)

        def keypress_with_shift(event) -> None:
            """
            Initializer of some keys (see codes).
            Инициализатор некоторых клавишь(см. коды).
            """
            if event.keycode == 83 or event.keycode == 115:
                self.save_as_file()

        self.bind_all("<Control-Shift-KeyPress>", keypress_with_shift)

        self.filetypes = (
            ('Text files', '.txt'),
            ('All files', '.*')
        )

        self.index_first = 0.0
        self.last_index = 0.0
        self.filepath_open = None

    def exit_from_editor(self) -> None:
        """
        Exiting the application.
        Выход из приложения.
        """
        self.master.title("SimplyApp - closing")
        self.master.destroy()

    def info(self):
        """
        For the function 'askyesno'.
        Для функции 'askyesno'.
        """
        title = "Save"
        massage = "Save the file?"
        return messagebox.askyesno(title, massage)

    def select_and_open_file(self) -> None:
        """
        Selecting and opening a file.
        Выбор и открытие файла.
        """
        self.filepath_open = (filedialog.askopenfilename
                              (filetypes=self.filetypes,
                               defaultextension=''))
        self.master.title(f"SimplyApp - {self.filepath_open}")
        if self.filepath_open:
            with open(self.filepath_open, "r") as outFile:
                self.txt_notes.delete("1.0", "end-1c")
                self.txt_notes.insert("1.0", outFile.read())
                outFile.close()

    def local(self) -> None:
        """
        To reset the variable.
        Чтобы сбросить переменную.
        """
        return None

    def new_file(self) -> None:
        """
        Creating a new text field.
        Создание нового текстового поля.
        """
        if self.filepath_open:
            flag = self.info()
            if flag:
                self.save_file()
                self.txt_notes.delete("1.0", "end-1c")
                self.filepath_open = None
            else:
                self.txt_notes.delete("1.0", "end-1c")
                self.filepath_open = None
        else:
            flag = self.info()
            if flag:
                self.save_as_file()
            self.txt_notes.delete("1.0", "end-1c")
        self.master.title("SimplyApp - New")

    def save_as_file(self) -> None:
        """
        The 'save as...' function.
        Функция "сохранить как...".
        """
        self.filepath_open = (filedialog.asksaveasfilename
                              (filetypes=self.filetypes,
                               defaultextension='initialfile'))
        if self.filepath_open:
            self.master.title(f"SimplyApp - {self.filepath_open}")
            with open(self.filepath_open, "w") as inFile:
                inFile.write(self.txt_notes.get("1.0", "end-1c"))
                inFile.close()

    def save_file(self) -> None:
        """
        The 'save' function.
        Функция "сохранить".
        """
        if self.filepath_open:
            self.master.title(f"SimplyApp - {self.filepath_open}")
            with open(self.filepath_open, "w") as outInfile:
                outInfile.write(self.txt_notes.get("1.0", "end-1c"))
                outInfile.close()
        else:
            self.save_as_file()

    def func_for_copy_cut(self) -> bool:
        """
        General function for copying and cutting.
        Общая функция для копирования и резки.
        """
        self.clipboard_append('')
        self.clipboard_clear()
        self.clipboard_append(self.txt_notes.selection_get())
        self.update()
        self.index_first = self.txt_notes.index("sel.first")
        self.index_last = self.txt_notes.index("sel.last")
        self.txt_notes.selection_clear()

    def cut_text(self) -> None:
        """
        Cut text.
        Вырезать текст.
        """
        self.func_for_copy_cut()
        self.txt_notes.delete(self.index_first, self.index_last)

    def copy_text(self) -> None:
        """
        Copy text.
        Копировать текст.
        """
        self.func_for_copy_cut()

    def paste_text(self):
        """
        Paste text.
        Вставить текст.
        """
        index_cursor = self.txt_notes.index('insert')
        self.txt_notes.insert(index_cursor, self.clipboard_get())

    def select_text(self) -> None:
        """
        Select text.
        Выбрать текст.
        """
        self.txt_notes.tag_add("sel", "1.0", "end-1c")

    connect_sql()


def main():
    """
    Main function.
    Главная функция.
    """
    root = Tk()
    TextEditor(root).pack()
    root.mainloop()


if __name__ == "__main__":
    main()
