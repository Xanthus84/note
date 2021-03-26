import gi
import ctypes
import commands

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

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


def print_bookmarks(bookmarks):  # вывод таблицы в закладку
    if notebook.get_current_page() == 0:  # загрузка в таблицы в закладку срочных дел
        for software_ref in bookmarks:
            lStore_now.append(list(software_ref))
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
    # print(count_width)
    # print(count_height)
    # print(max(page))
    # print(count_width)
    global inc
    Window.resize(count_width + 150, max(page) * 23 + 180)
    # sWindow_now.set_resize_mode(Window)
    inc = 0


sort_now = dict()
sort_medium = dict()
sort_perspective = dict()


def rename_number_cell(data):  # функция сокрытия автоинкремента номера id строк таблицы на на нумерацию, начиная с 1
    if data == 'bookmarks':
        for i in range(len(lStore_now)):  # цикл по значениям списка
            path = Gtk.TreePath(i)  # перебор строк с присвоением в path
            treeiter = lStore_now.get_iter(path)  # получение iter, соответствующее path
            sort_now[i + 1] = lStore_now.get_value(treeiter, 0)  # изменяет значение первого столбца в
            lStore_now.set_value(treeiter, 0, list(sort_now.keys())[i])
            # заданной строке тестом из поля entry
    if data == 'bookmarks_medium':
        for i in range(len(lStore_medium)):  # цикл по значениям списка
            path = Gtk.TreePath(i)  # перебор строк с присвоением в path
            treeiter = lStore_medium.get_iter(path)  # получение iter, соответствующее path
            sort_medium[i + 1] = lStore_medium.get_value(treeiter, 0)  # изменяет значение первого столбца в
            lStore_medium.set_value(treeiter, 0, list(sort_medium.keys())[i])
            # заданной строке тестом из поля entry
    if data == 'bookmarks_perspective':
        for i in range(len(lStore_perspective)):  # цикл по значениям списка
            path = Gtk.TreePath(i)  # перебор строк с присвоением в path
            treeiter = lStore_perspective.get_iter(path)  # получение iter, соответствующее path
            sort_perspective[i + 1] = lStore_perspective.get_value(treeiter, 0)  # изменяет значение первого столбца в
            lStore_perspective.set_value(treeiter, 0, list(sort_perspective.keys())[i])
            # заданной строке тестом из поля entry

    # for j in sort_now:
    #         #     path = Gtk.TreePath(j)  # перебор строк с присвоением в path
    #         #     treeiter = lStore_now.get_iter(path)  # получение iter, соответствующее path
    #         #     lStore_now.set_value(treeiter, 0, j+1)


class Option:  # подключение текста меню к командам бизнес-логики
    def __init__(self, name, command, prep_call=None):
        self.name = name  # <1> имя, показываемое в меню
        self.command = command  # <2> экземпляр выполняемой программы
        self.prep_call = prep_call  # <3> необязательный подготовительный шаг, который вызывается перед выполнением
        # программы

    def _handle_message(self, message):  # функция проверки формата данных, если список то вызов print_bookmarks
        if isinstance(message, list):
            print_bookmarks(message)
        else:
            entry_sabject.set_text(message)

    def choose(self, name):  # <4> вызывается, когда вариант действия выбран из меню
        data = self.prep_call() if self.prep_call else None  # <5> вызывает подготовительный шаг, если он указан
        message = self.command.execute(
            name, data) if data else self.command.execute(name)  # <6> выполняет команду, переданную в данных из
        # подготовительного шага
        self._handle_message(message)

    def choose_update(self, name):  # <4> вызывается, когда вариант действия выбран из меню
        note = entry.get_text()
        data = self.prep_call() if self.prep_call else None  # <5> вызывает подготовительный шаг, если он указан
        message = self.command.execute(
            name, data, note) if data else self.command.execute(name)  # <6> выполняет команду, переданную в данных из
        # подготовительного шага
        self._handle_message(message)

    def choose_first_add(self, name):
        message = self.command.execute(name)
        get_width_height(message)

    # def __str__(self):  # <7> представляет вариант действия в формате имени вместо дефолтного поведения Python
    #     return self.name


# def on_tree_selection_changed(selection):  # функция показывает значение в выделенном пользователем столбце и строке
#     model, treeiter = selection.get_selected()
#     if treeiter is not None:
#         print("You selected", model[treeiter][1])

# name_note_dict = {
#     'title': 'Заметка1',
#     'url': 'Address',
#     'notes': 'note1'
# }
#
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

        Option('Add a bookmark', commands.AddBookmarkCommand(), prep_call=get_new_bookmark_data).choose(
            get_table_name())
        clear_table()
        Option('List bookmarks by date', commands.ListBookmarksCommand()).choose(get_table_name())

        rename_number_cell(get_table_name())

    def change_note_clicked_cb(self, button):  # обрабатывает нажатие кнопки "Изменить запись"
        global count_width
        if int(get_bookmark_id_for_deletion()) > 0:
            if GetTextDimensions(entry.get_text(), 11, "Cantarell") > count_width:
                count_width = GetTextDimensions(entry.get_text(), 11, "Cantarell")
                resize_window()
            else:
                count_width = 0
                Option('List bookmarks by date', commands.ListBookmarksCommand()).choose_first_add('bookmarks')
                Option('List bookmarks by date', commands.ListBookmarksCommand()).choose_first_add('bookmarks_medium')
                Option('List bookmarks by date', commands.ListBookmarksCommand()).choose_first_add(
                    'bookmarks_perspective')
                resize_window()

            Option('Update a bookmark', commands.UpdateBookmarkCommand(),
                   prep_call=get_bookmark_id_for_deletion).choose_update(get_table_name())
            clear_table()
            Option('List bookmarks by date', commands.ListBookmarksCommand()).choose(get_table_name())

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
                   prep_call=get_bookmark_id_for_deletion).choose(get_table_name())
            clear_table()
            Option('List bookmarks by date', commands.ListBookmarksCommand()).choose(get_table_name())

            rename_number_cell(get_table_name())
        else:
            entry_sabject.set_text("Выделите заметку!")


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

# sWindow_now.set_hexpand(True)
# sWindow_now.set_vexpand(True)
# sWindow_medium.set_hexpand(True)
# sWindow_medium.set_vexpand(True)
# text_now = abuilder.get_object("text_now")
# textbuffer = text_now.get_buffer()
# textbuffer.set_text('123')
lStore_now = abuilder.get_object("liststore_now")
lStore_medium = abuilder.get_object("liststore_medium")
lStore_perspective = abuilder.get_object("liststore_perspective")
# lStore_now = Gtk.ListStore(int, str, str)

tree_now = abuilder.get_object("tree_view_now")
tree_medium = abuilder.get_object("tree_view_medium")
tree_perspective = abuilder.get_object("tree_view_perspective")
# tree_now.set_hexpand(True)
# tree_now.set_vexpand(True)
# tree_medium.set_hexpand(True)
# tree_medium.set_vexpand(True)
for i, column_title in enumerate(  # загрузка в дерево столбцов и присвоение им наименований
        ["№", "Список срочных дел", "Дата"]
):
    renderer = Gtk.CellRendererText()
    column = Gtk.TreeViewColumn(column_title, renderer, text=i)
    tree_now.append_column(column)

for i, column_title in enumerate(  # загрузка в дерево столбцов и присвоение им наименований
        ["№", "Список среднесрочных дел", "Дата"]
):
    renderer = Gtk.CellRendererText()
    column = Gtk.TreeViewColumn(column_title, renderer, text=i)
    tree_medium.append_column(column)

for i, column_title in enumerate(  # загрузка в дерево столбцов и присвоение им наименований
        ["№", "Список перспективных дел", "Дата"]
):
    renderer = Gtk.CellRendererText()
    column = Gtk.TreeViewColumn(column_title, renderer, text=i)
    tree_perspective.append_column(column)

# select = tree_now.get_selection()  # выбор таблицы
# select.connect("changed", on_tree_selection_changed)  # подключение сигнала выбранной строки


# sWindow_now.add(tree_now)

Window.show_all()
# whatis(Window)
if __name__ == '__main__':
    commands.CreateBookmarksTableCommand().execute('bookmarks')  # инициализация БД
    # получение данных их таблиц для изменения размеров окна под содержимое
    Option('List bookmarks by date', commands.ListBookmarksCommand()).choose_first_add('bookmarks')
    Option('List bookmarks by date', commands.ListBookmarksCommand()).choose_first_add('bookmarks_medium')
    Option('List bookmarks by date', commands.ListBookmarksCommand()).choose_first_add('bookmarks_perspective')
    resize_window()  # функция изменения размеров окна под содержимое таблиц

    Option('List bookmarks by date', commands.ListBookmarksCommand()).choose(
        'bookmarks')  # загрузка таблицы bookmarks в 1-ю вкладку
    notebook.next_page()  # переход на вторую вкладку
    Option('List bookmarks by date', commands.ListBookmarksCommand()).choose(
        'bookmarks_medium')  # загрузка таблицы bookmarks_medium во 2-ю вкладку
    notebook.next_page()  # переход на третью вкладку
    Option('List bookmarks by date', commands.ListBookmarksCommand()).choose(
        'bookmarks_perspective')  # загрузка таблицы bookmarks_perspective в 3-ю вкладку
    notebook.set_current_page(0)  # возвращение на первую вкладку

    rename_number_cell('bookmarks')  # переименование строк в столбце для скрытия id
    rename_number_cell('bookmarks_medium')  # переименование строк в столбце для скрытия id
    rename_number_cell('bookmarks_perspective')  # переименование строк в столбце для скрытия id

    entry_sabject.set_text("Таблицы загружены")  # вывод надписи в нижнее поле
    Gtk.main()
