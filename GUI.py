#!C:/msys64/mingw64/bin/python.exe
import gi
import ctypes
import commands
import keyboard

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

whatis = lambda obj: print(type(obj), "\n\t" + "\n\t".join(dir(obj)))


def GetTextDimensions(text, points, font):  # считает ширину текста в пикселах
    class SIZE(ctypes.Structure):
        _fields_ = [("cx", ctypes.c_long), ("cy", ctypes.c_long)]

    hdc = ctypes.windll.user32.GetDC(0)
    hfont = ctypes.windll.gdi32.CreateFontA(points, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, font)
    hfont_old = ctypes.windll.gdi32.SelectObject(hdc, hfont)

    size = SIZE(0, 0)
    ctypes.windll.gdi32.GetTextExtentPoint32A(hdc, text, len(text), ctypes.byref(size))

    ctypes.windll.gdi32.SelectObject(hdc, hfont_old)
    ctypes.windll.gdi32.DeleteObject(hfont)

    return size.cx  # возвращает ширину строки size.cx и высоту строки size.cy [size.cx, size.cy]


# lStore_now_save = []


def print_bookmarks(bookmarks):  # вывод таблицы в закладку
    if notebook.get_current_page() == 0:  # загрузка в таблицы в закладку срочных дел
        for software_ref in bookmarks:
            lStore_now.append(list(software_ref))
            # lStore_now_save.append(list(software_ref))
    if notebook.get_current_page() == 1:  # загрузка в таблицы в закладку среднесрочных дел
        for software_ref in bookmarks:
            lStore_medium.append(list(software_ref))
    if notebook.get_current_page() == 2:  # загрузка в таблицы в закладку среднесрочных дел
        for software_ref in bookmarks:
            lStore_perspective.append(list(software_ref))


count_width = 0  # глобальная переменная максимальной ширины строки
count_height = 0  # глобальная переменная максимальной высоты строки
inc = 0  # переменная для определения вкладки высоты таблиц page
page = [0, 0, 0]  # список для высоты таблиц


def get_width_height(bookmarks):  # расчет наибольшей высоты таблиц и наибольшей ширины строки в таблицах
    global count_width
    global count_height
    global page
    global inc
    count_w = 0
    count_h = 0
    for software_ref in bookmarks:  # построчный проход по таблице
        count_h = count_h + 1  # подсчет количества строк в таблице
        for row in list(software_ref):  # проход по каждому столбцу в строке таблицы
            # print(GetTextDimensions(str(row), 11, "Cantarell"))
            if count_w < GetTextDimensions(str(row), 11, "Cantarell"):  # сравнение переменой с шириной значения столбца
                count_w = GetTextDimensions(str(row), 11, "Cantarell")  # присвоение переменной максимальной величины
                # ширины столбца
    if count_width < count_w:  # присвоение глобальной переменной максимальной величины ширины столбца
        count_width = count_w
    if count_height < count_h:  # присвоение глобальной переменной максимального рамера строк
        count_height = count_h
    page[inc] = count_h  # занесение в список значений высоты каждой таблицы
    inc = inc + 1


def resize_window():  # функция изменения размера окна, в зависимости от количества строк и максимальной ширины строки
    global count_width
    global count_height
    global inc
    Window.resize(count_width + 150, max(page) * 23 + 180)
    inc = 0


sort_now = dict()
sort_medium = dict()
sort_perspective = dict()


def rename_number_cell(data):  # функция сокрытия автоинкремента номера id строк таблицы на на нумерацию, начиная с 1
    if data == 'bookmarks':
        for i in range(len(lStore_now)):  # цикл по значениям списка
            path = Gtk.TreePath(i)  # перебор строк с присвоением в path
            treeiter = lStore_now.get_iter(path)  # получение iter, соответствующее path
            sort_now[i + 1] = lStore_now.get_value(treeiter, 0)  # присваивает ключу словаря значение столбца id
            lStore_now.set_value(treeiter, 0,
                                 list(sort_now.keys())[i])  # устанавливает маску с порядковым номером на id

    if data == 'bookmarks_medium':
        for i in range(len(lStore_medium)):  # цикл по значениям списка
            path = Gtk.TreePath(i)  # перебор строк с присвоением в path
            treeiter = lStore_medium.get_iter(path)  # получение iter, соответствующее path
            sort_medium[i + 1] = lStore_medium.get_value(treeiter, 0)  # присваивает ключу словаря значение столбца id
            lStore_medium.set_value(treeiter, 0,
                                    list(sort_medium.keys())[i])  # устанавливает маску с порядковым номером на id

    if data == 'bookmarks_perspective':
        for i in range(len(lStore_perspective)):  # цикл по значениям списка
            path = Gtk.TreePath(i)  # перебор строк с присвоением в path
            treeiter = lStore_perspective.get_iter(path)  # получение iter, соответствующее path
            sort_perspective[i + 1] = lStore_perspective.get_value(treeiter,
                                                                   0)  # присваивает ключу словаря значение столбца id
            lStore_perspective.set_value(treeiter, 0, list(sort_perspective.keys())[
                i])  # устанавливает маску с порядковым номером на id


def format_bookmark(bookmark):
    return '\t'.join(
        str(field) if field else ''
        for field in bookmark
    )


class Option:  # подключение текста меню к командам бизнес-логики
    def __init__(self, name, command, prep_call=None, success_message='{result}'):
        self.name = name  # <1> имя, показываемое в меню
        self.command = command  # <2> экземпляр выполняемой программы
        self.prep_call = prep_call  # <3> необязательный подготовительный шаг, который вызывается перед выполнением
        # программы
        self.success_message = success_message  # сообщение о выполнении программы

    def choose(self, name, note=None):  # <4> вызывается, когда вариант действия выбран из меню
        if self.prep_call:
            if self.name != 'Edit a bookmark':
                note = entry.get_text()
            data = self.prep_call()
        else:
            data = None  # <5> вызывает подготовительный шаг, если он указан
        success, result = self.command.execute(name, data, note)  # <3>
        formatted_result = ""
        if isinstance(result, list):  # <4>
            print_bookmarks(result)
        else:
            formatted_result = self.success_message
            if formatted_result == 'Заметка удалена!':
                entry_sabject.set_text(formatted_result)
                entry_sabject.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse("red"))
            else:
                entry_sabject.set_text(formatted_result)
                entry_sabject.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse("green"))
        if success:
            # print(self.success_message.format(result=formatted_result))
            entry_sabject.set_text(self.success_message.format(result=formatted_result))

def on_tree_selection_changed(selection):  # функция показывает значение в выделенном пользователем столбце и строке
    model, treeiter = selection.get_selected()
    if treeiter is not None:
        print("You selected", model[treeiter][1])


def get_user_input(label):  # <1> общая функция, которая предлагает пользователя ввести данные
    return entry.get_text()


def get_new_bookmark_data():  # <4> функция, которая получает необходимые данные для добавления новой закладки
    return {
        'title': get_user_input('Title'),
        # 'url': 'Address',
        # 'notes': 'note1',  # <5> примечания для закладки не являются обязательными,
        # # поэтому не продолжает предлагать их ввести
    }


def get_bookmark_id_for_deletion():  # <6> получает необходимую информацию для удаления закладки
    selection_now = tree_now.get_selection()
    selection_medium = tree_medium.get_selection()
    selection_perspective = tree_perspective.get_selection()
    num = selection_now.count_selected_rows() + selection_medium.count_selected_rows() + selection_perspective.count_selected_rows()
    if num > 0:  # проверка выделена ли строка в одной из таблиц
        if notebook.get_current_page() == 0:
            for i in range(len(lStore_now)):
                path = Gtk.TreePath(i)
                treeiter = lStore_now.get_iter(path)
                if selection_now.iter_is_selected(treeiter) == True:
                    return str(sort_now[lStore_now.get_value(treeiter, 0)])
        if notebook.get_current_page() == 1:
            for i in range(len(lStore_medium)):
                path = Gtk.TreePath(i)
                treeiter = lStore_medium.get_iter(path)
                if selection_medium.iter_is_selected(treeiter) == True:
                    return str(sort_medium[lStore_medium.get_value(treeiter, 0)])
        if notebook.get_current_page() == 2:
            for i in range(len(lStore_perspective)):
                path = Gtk.TreePath(i)
                treeiter = lStore_perspective.get_iter(path)
                if selection_perspective.iter_is_selected(treeiter) == True:
                    return str(sort_perspective[lStore_perspective.get_value(treeiter, 0)])
    else:
        return 0


def clear_table():  # функция очистки таблицы
    if notebook.get_current_page() == 0:  # если выбрана таблица срочных дел bookmarks
        lStore_now.clear()
    if notebook.get_current_page() == 1:  # если выбрана таблица среднесрочных дел bookmarks_medium
        lStore_medium.clear()
    if notebook.get_current_page() == 2:  # если выбрана таблица перспективных дел bookmarks_perspective
        lStore_perspective.clear()


def get_table_name():  # функция возвращает наименование текущей таблицы
    if notebook.get_current_page() == 0:  # добавление заметки в таблицу срочных дел bookmarks
        # lStore_now.clear()
        return 'bookmarks'
    if notebook.get_current_page() == 1:  # добавление заметки в таблицу среднесрочных дел bookmarks_medium
        # lStore_medium.clear()
        return 'bookmarks_medium'
    if notebook.get_current_page() == 2:  # добавление заметки в таблицу среднесрочных дел bookmarks_perspective
        # lStore_perspective.clear()
        return 'bookmarks_perspective'


class Handler:

    def get_note_clicked_cb(self, button):  # обрабатывает нажатие кнопки "Добавить запись"
        global count_width
        global count_height
        global page
        if notebook.get_current_page() == 0 and page[0] == max(
                page):  # добавление заметки в таблицу срочных дел bookmarks
            count_height = count_height + 1
            if GetTextDimensions(entry.get_text(), 11, "Cantarell") > count_width:
                count_width = GetTextDimensions(entry.get_text(), 11, "Cantarell")
            page[0] = page[0] + 1
            resize_window()
        elif notebook.get_current_page() == 1 and page[1] == max(
                page):  # добавление заметки в таблицу среднесрочных дел bookmarks_medium
            count_height = count_height + 1
            if GetTextDimensions(entry.get_text(), 11, "Cantarell") > count_width:
                count_width = GetTextDimensions(entry.get_text(), 11, "Cantarell")
            page[1] = page[1] + 1
            resize_window()
        elif notebook.get_current_page() == 2 and page[2] == max(
                page):  # добавление заметки в таблицу среднесрочных дел bookmarks_perspective
            count_height = count_height + 1
            if GetTextDimensions(entry.get_text(), 11, "Cantarell") > count_width:
                count_width = GetTextDimensions(entry.get_text(), 11, "Cantarell")
            page[2] = page[2] + 1
            resize_window()
        else:
            if notebook.get_current_page() == 0:  # добавление заметки в таблицу срочных дел bookmarks
                page[0] = page[0] + 1
                if GetTextDimensions(entry.get_text(), 11, "Cantarell") > count_width:
                    count_width = GetTextDimensions(entry.get_text(), 11, "Cantarell")
            elif notebook.get_current_page() == 1:  # добавление заметки в таблицу среднесрочных дел bookmarks_medium
                page[1] = page[1] + 1
                if GetTextDimensions(entry.get_text(), 11, "Cantarell") > count_width:
                    count_width = GetTextDimensions(entry.get_text(), 11, "Cantarell")
            elif notebook.get_current_page() == 2:  # добавление заметки в таблицу среднесрочных дел bookmarks_perspective
                page[2] = page[2] + 1
                if GetTextDimensions(entry.get_text(), 11, "Cantarell") > count_width:
                    count_width = GetTextDimensions(entry.get_text(), 11, "Cantarell")

        Option('Add a bookmark', commands.AddBookmarkCommand(), prep_call=get_new_bookmark_data,
               success_message='Заметка добавлена!').choose(
            get_table_name())
        clear_table()
        Option('List bookmarks by date', commands.ListBookmarksCommand(),
               success_message='Заметка добавлена!').choose(get_table_name())

        rename_number_cell(get_table_name())

    def change_note_clicked_cb(self, button):  # обрабатывает нажатие кнопки "Изменить запись"
        global count_width
        if int(get_bookmark_id_for_deletion()) > 0:
            if GetTextDimensions(entry.get_text(), 11, "Cantarell") > count_width:
                count_width = GetTextDimensions(entry.get_text(), 11, "Cantarell")
                resize_window()
            else:
                # get_width_height(get_table_name())
                resize_window()

            Option('Update a bookmark', commands.UpdateBookmarkCommand(),
                   prep_call=get_bookmark_id_for_deletion, success_message='Заметка обновлена!').choose(
                get_table_name())
            clear_table()
            Option('List bookmarks by date', commands.ListBookmarksCommand(),
                   success_message='Заметка обновлена!').choose(get_table_name())

            rename_number_cell(get_table_name())
        else:
            entry_sabject.set_text("Выделите заметку!")

    def delete_note_clicked_cb(self, button):  # обрабатывает нажатие кнопки "Изменить запись"
        global count_width
        global count_height
        global page
        if int(get_bookmark_id_for_deletion()) > 0:
            if notebook.get_current_page() == 0 and page[0] == max(
                    page):  # добавление заметки в таблицу срочных дел bookmarks
                count_height = count_height - 1
                page[0] = page[0] - 1
                resize_window()
            elif notebook.get_current_page() == 1 and page[1] == max(
                    page):  # добавление заметки в таблицу среднесрочных дел bookmarks_medium
                count_height = count_height - 1
                page[1] = page[1] - 1
                resize_window()
            elif notebook.get_current_page() == 2 and page[2] == max(
                    page):  # добавление заметки в таблицу среднесрочных дел bookmarks_perspective
                count_height = count_height - 1
                page[2] = page[2] - 1
                resize_window()
            else:
                if notebook.get_current_page() == 0:  # добавление заметки в таблицу срочных дел bookmarks
                    page[0] = page[0] - 1
                elif notebook.get_current_page() == 1:  # добавление заметки в таблицу среднесрочных дел bookmarks_medium
                    page[1] = page[1] - 1
                elif notebook.get_current_page() == 2:  # добавление заметки в таблицу среднесрочных дел bookmarks_perspective
                    page[2] = page[2] - 1

            Option('Delete a bookmark', commands.DeleteBookmarkCommand(),
                   prep_call=get_bookmark_id_for_deletion, success_message='Заметка удалена!').choose(get_table_name())
            clear_table()
            Option('List bookmarks by date', commands.ListBookmarksCommand(),
                   success_message='Заметка удалена!').choose(get_table_name())
            rename_number_cell(get_table_name())
        else:
            entry_sabject.set_text("Выделите заметку!")
            entry_sabject.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse("red"))

    def main_window_key_press_event_cb(self, window, event):  # функция анализ нажатия кнопок в главном окне
        keyname = Gdk.keyval_name(event.keyval)  # получаем наименование нажатой кнопки
        if keyname == "Down":  # если нажата стрелка вниз
            selection_now = tree_now.get_selection()  # получаем выделение
            selection_medium = tree_medium.get_selection()  # получаем выделение
            selection_perspective = tree_perspective.get_selection()  # получаем выделение
            if notebook.get_current_page() == 0:  # проверяем какая страница выбрана
                path = Gtk.TreePath(len(lStore_now) - 1)  # определяем path последней строки списка
                treeiter = lStore_now.get_iter(path)  # определяем treeiter последней строки списка
                if selection_now.iter_is_selected(treeiter) == True:  # определяем выделена ли последняя строка списка
                    self.get_note_clicked_cb("Insert_new_note")  # добавляем новую строку
                    # переводим курсор на добавленную строку
                    last = lStore_now.iter_n_children()
                    last = last - 1
                    c = tree_now.get_column(0)
                    tree_now.set_cursor(last, c, True)
            elif notebook.get_current_page() == 1:  # проверяем какая страница выбрана
                path = Gtk.TreePath(len(lStore_medium) - 1)  # определяем path последней строки списка
                treeiter = lStore_medium.get_iter(path)  # определяем treeiter последней строки списка
                if selection_medium.iter_is_selected(
                        treeiter) == True:  # определяем выделена ли последняя строка списка
                    self.get_note_clicked_cb("Insert_new_note")  # добавляем новую строку
                    # переводим курсор на добавленную строку
                    last = lStore_medium.iter_n_children()
                    last = last - 1
                    c = tree_medium.get_column(0)
                    tree_medium.set_cursor(last, c, True)
            elif notebook.get_current_page() == 2:  # проверяем какая страница выбрана
                path = Gtk.TreePath(len(lStore_perspective) - 1)  # определяем path последней строки списка
                treeiter = lStore_perspective.get_iter(path)  # определяем treeiter последней строки списка
                if selection_perspective.iter_is_selected(
                        treeiter) == True:  # определяем выделена ли последняя строка списка
                    self.get_note_clicked_cb("Insert_new_note")  # добавляем новую строку
                    # переводим курсор на добавленную строку
                    last = lStore_perspective.iter_n_children()
                    last = last - 1
                    c = tree_perspective.get_column(0)
                    tree_perspective.set_cursor(last, c, True)

        if keyname == "Delete":
            self.delete_note_clicked_cb("Delete_note")


def text_edited(widget, path, text):  # функция записи во второй столбец таблицы редактируемого значения
    global count_width

    if notebook.get_current_page() == 0:  # добавление заметки в таблицу срочных дел bookmarks
        lStore_now[path][1] = text
    elif notebook.get_current_page() == 1:  # добавление заметки в таблицу среднесрочных дел bookmarks_medium
        lStore_medium[path][1] = text
    elif notebook.get_current_page() == 2:  # добавление заметки в таблицу среднесрочных дел bookmarks_perspective
        lStore_perspective[path][1] = text

    if GetTextDimensions(text, 11, "Cantarell") > count_width:
        count_width = GetTextDimensions(text, 11, "Cantarell")
        resize_window()
    else:
        # get_width_height(get_table_name())
        resize_window()
    Option('Edit a bookmark', commands.UpdateBookmarkCommand(),
           prep_call=get_bookmark_id_for_deletion, success_message='Заметка обновлена!').choose(get_table_name(), text)
    clear_table()
    Option('List bookmarks by date', commands.ListBookmarksCommand(), success_message='Заметка обновлена!').choose(
        get_table_name())
    rename_number_cell(get_table_name())


abuilder = Gtk.Builder()
abuilder.add_from_file("Interfeice.glade")
abuilder.connect_signals(Handler())

Window = abuilder.get_object("main_window")
Window.connect("destroy", Gtk.main_quit)
Window.set_resizable(True)
Window.set_default_size(300, 600)

entry = abuilder.get_object("entry_insert")
entry_sabject = abuilder.get_object("entry_sabj")

notebook = abuilder.get_object("note_book")
sWindow_now = abuilder.get_object("scrolled_window_now")  # окно прокрутки первой вкладки
sWindow_medium = abuilder.get_object("scrolled_window_medium")  # окно прокрутки первой вкладки
sWindow_perspective = abuilder.get_object("scrolled_window_perspective")  # окно прокрутки первой вкладки

lStore_now = abuilder.get_object("liststore_now")
lStore_medium = abuilder.get_object("liststore_medium")
lStore_perspective = abuilder.get_object("liststore_perspective")
# lStore_now = Gtk.ListStore(int, str, str)

tree_now = abuilder.get_object("tree_view_now")
tree_medium = abuilder.get_object("tree_view_medium")
tree_perspective = abuilder.get_object("tree_view_perspective")

for i, column_title in enumerate(  # загрузка в дерево столбцов и присвоение им наименований
        ["№", "Список срочных дел", "Дата"]
):
    renderer = Gtk.CellRendererText()
    column = Gtk.TreeViewColumn(column_title, renderer, text=i)
    tree_now.append_column(column)
    if i == 1:
        renderer.set_property("editable", True)  # делает редактируемым строки столбца 1
        renderer.connect("edited", text_edited)  # запоминает введенное значение в строку

for i, column_title in enumerate(  # загрузка в дерево столбцов и присвоение им наименований
        ["№", "Список среднесрочных дел", "Дата"]
):
    renderer = Gtk.CellRendererText()
    column = Gtk.TreeViewColumn(column_title, renderer, text=i)
    tree_medium.append_column(column)
    if i == 1:
        renderer.set_property("editable", True)  # делает редактируемым строки столбца 1
        renderer.connect("edited", text_edited)  # запоминает введенное значение в строку

for i, column_title in enumerate(  # загрузка в дерево столбцов и присвоение им наименований
        ["№", "Список перспективных дел", "Дата"]
):
    renderer = Gtk.CellRendererText()
    column = Gtk.TreeViewColumn(column_title, renderer, text=i)
    tree_perspective.append_column(column)
    if i == 1:
        renderer.set_property("editable", True)  # делает редактируемым строки столбца 1
        renderer.connect("edited", text_edited)  # запоминает введенное значение в строку

Window.set_title("ToDoIt")
Window.set_icon_from_file("icon.ico")
Window.show_all()
whatis(Gtk.ToolButton)

if __name__ == '__main__':
    Option('List bookmarks by date', commands.ListBookmarksCommand(),
           success_message='Таблицы загружены!').choose(
        'bookmarks')  # загрузка таблицы bookmarks в 1-ю вкладку
    notebook.next_page()  # переход на вторую вкладку
    Option('List bookmarks by date', commands.ListBookmarksCommand(),
           success_message='Таблицы загружены!').choose(
        'bookmarks_medium')  # загрузка таблицы bookmarks_medium во 2-ю вкладку
    notebook.next_page()  # переход на третью вкладку
    Option('List bookmarks by date', commands.ListBookmarksCommand(),
           success_message='Таблицы загружены!').choose(
        'bookmarks_perspective')  # загрузка таблицы bookmarks_perspective в 3-ю вкладку
    notebook.set_current_page(0)  # возвращение на первую вкладку
    rename_number_cell('bookmarks')  # переименование строк в столбце для скрытия id
    rename_number_cell('bookmarks_medium')  # переименование строк в столбце для скрытия id
    rename_number_cell('bookmarks_perspective')  # переименование строк в столбце для скрытия id
    get_width_height("bookmarks")
    get_width_height("bookmarks_medium")
    get_width_height("bookmarks_perspective")  # функция изменения размеров окна под содержимое таблиц
    # print(lStore_now_save)
    Gtk.main()
