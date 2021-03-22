import gi
from gi.overrides.Gtk import TextBuffer
import os
from collections import OrderedDict

import commands

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

whatis = lambda obj: print(type(obj), "\n\t" + "\n\t".join(dir(obj)))


# def print_bookmarks(bookmarks): #  вывод таблицы в командную строку
#     for bookmark in bookmarks:
#         print('\t'.join(
#             str(field) if field else ''
#             for field in bookmark
#         ))

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


class Option:  # подключение текста меню к командам бизнес-логики
    def __init__(self, name, command, prep_call=None):
        self.name = name  # <1> имя, показываемое в меню
        self.command = command  # <2> экземпляр выполняемой программы
        self.prep_call = prep_call  # <3> необязательный подготовительный шаг, который вызывается перед выполнением
        # программы

    def _handle_message(self, message):
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

    def __str__(self):  # <7> представляет вариант действия в формате имени вместо дефолтного поведения Python
        return self.name


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


#
# def get_new_bookmark_data():  # <4> функция, которая получает необходимые данные для добавления новой закладки
#     return {
#         'title': get_user_input('Title'),
#         'url': get_user_input('URL'),
#         'notes': get_user_input('Notes'),  # <5> примечания для закладки не являются обязательными,
#         # поэтому не продолжает предлагать их ввести
#     }

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
                    return str(lStore_now.get_value(treeiter, 0))
        if notebook.get_current_page() == 1:
            for i in range(len(lStore_medium)):
                path = Gtk.TreePath(i)
                treeiter = lStore_medium.get_iter(path)
                if selection_medium.iter_is_selected(treeiter) == True:
                    return str(lStore_medium.get_value(treeiter, 0))
        if notebook.get_current_page() == 2:
            for i in range(len(lStore_perspective)):
                path = Gtk.TreePath(i)
                treeiter = lStore_perspective.get_iter(path)
                if selection_perspective.iter_is_selected(treeiter) == True:
                    return str(lStore_perspective.get_value(treeiter, 0))
    else:
        return '0'


class Handler:
    def get_note_clicked_cb(self, button):
        if notebook.get_current_page() == 0:  # добавление заметки в таблицу срочных дел bookmarks
            Option('Add a bookmark', commands.AddBookmarkCommand(), prep_call=get_new_bookmark_data).choose('bookmarks')
            lStore_now.clear()
            Option('List bookmarks by date', commands.ListBookmarksCommand()).choose('bookmarks')
        if notebook.get_current_page() == 1:  # добавление заметки в таблицу среднесрочных дел bookmarks_medium
            Option('Add a bookmark', commands.AddBookmarkCommand(), prep_call=get_new_bookmark_data).choose('bookmarks_medium')
            lStore_medium.clear()
            Option('List bookmarks by date', commands.ListBookmarksCommand()).choose('bookmarks_medium')
        if notebook.get_current_page() == 2:  # добавление заметки в таблицу среднесрочных дел bookmarks_perspective
            Option('Add a bookmark', commands.AddBookmarkCommand(), prep_call=get_new_bookmark_data).choose('bookmarks_perspective')
            lStore_perspective.clear()
            Option('List bookmarks by date', commands.ListBookmarksCommand()).choose('bookmarks_perspective')
        # software_list = [len(lStore_now) + 1, entry.get_text()]
        # # for row in lStore_now:  # цикл вывода на печать всех значений списка
        # #     print(row[:])
        # lStore_now.append(list(software_list))

    def change_note_clicked_cb(self, button):
        if notebook.get_current_page() == 0:  # изменение заметки в таблице срочных дел bookmarks
            Option('Update a bookmark', commands.UpdateBookmarkCommand(),
                   prep_call=get_bookmark_id_for_deletion).choose_update('bookmarks')
            lStore_now.clear()
            Option('List bookmarks by date', commands.ListBookmarksCommand()).choose('bookmarks')
        if notebook.get_current_page() == 1:  # изменение заметки в таблице среднесрочных дел bookmarks
            Option('Update a bookmark', commands.UpdateBookmarkCommand(),
                   prep_call=get_bookmark_id_for_deletion).choose_update('bookmarks_medium')
            lStore_medium.clear()
            Option('List bookmarks by date', commands.ListBookmarksCommand()).choose('bookmarks_medium')
        if notebook.get_current_page() == 2:  # удаление заметки в таблице перспективных дел bookmarks
            Option('Update a bookmark', commands.UpdateBookmarkCommand(),
                   prep_call=get_bookmark_id_for_deletion).choose_update('bookmarks_perspective')
            lStore_perspective.clear()
            Option('List bookmarks by date', commands.ListBookmarksCommand()).choose('bookmarks_perspective')
        # selection = tree_now.get_selection()  # выбор таблицы
        # num = selection.count_selected_rows()  # проверка, выделена ли хотя бы одна строка
        # if num > 0:
        #     if not entry.get_text() == '':
        #         for i in range(len(lStore_now)):  # цикл по значениям списка
        #             path = Gtk.TreePath(i)  # перебор строк с присвоением в path
        #             treeiter = lStore_now.get_iter(path)  # получение iter, соответствующее path
        #             if selection.iter_is_selected(treeiter) == True:  # проверка условия, выделена ли строка
        #                 # print(lStore_now.get_value(treeiter, 1)) # получить значение первого столбца по заданной строке
        #                 lStore_now.set_value(treeiter, 1, entry.get_text())  # изменяет значение первого столбца в
        #                 # заданной строке тестом из поля entry
        #                 return

    # def rename_number_cell(self):
    #     for i in range(len(lStore_now)):  # цикл по значениям списка
    #         path = Gtk.TreePath(i)  # перебор строк с присвоением в path
    #         treeiter = lStore_now.get_iter(path)  # получение iter, соответствующее path
    #         lStore_now.set_value(treeiter, 0, i + 1)  # изменяет значение первого столбца в
    #         # заданной строке тестом из поля entry

    def delete_note_clicked_cb(self, button):
        if notebook.get_current_page() == 0:  # удаление заметки в таблице срочных дел bookmarks
            Option('Delete a bookmark', commands.DeleteBookmarkCommand(), prep_call=get_bookmark_id_for_deletion).choose('bookmarks')
            lStore_now.clear()
            Option('List bookmarks by date', commands.ListBookmarksCommand()).choose('bookmarks')
        if notebook.get_current_page() == 1:  # удаление заметки в таблице среднесрочных дел bookmarks
            Option('Delete a bookmark', commands.DeleteBookmarkCommand(),
                    prep_call=get_bookmark_id_for_deletion).choose('bookmarks_medium')
            lStore_medium.clear()
            Option('List bookmarks by date', commands.ListBookmarksCommand()).choose('bookmarks_medium')
        if notebook.get_current_page() == 2:  # удаление заметки в таблице перспективных дел bookmarks
            Option('Delete a bookmark', commands.DeleteBookmarkCommand(),
                    prep_call=get_bookmark_id_for_deletion).choose('bookmarks_perspective')
            lStore_perspective.clear()
            Option('List bookmarks by date', commands.ListBookmarksCommand()).choose('bookmarks_perspective')
        # selection = tree_now.get_selection()
        # num = selection.count_selected_rows()
        # if num > 0:
        #     for i in range(len(lStore_now)):
        #         path = Gtk.TreePath(i)
        #         treeiter = lStore_now.get_iter(path)
        #         if selection.iter_is_selected(treeiter) == True:
        #             lStore_now.remove(treeiter)
        #             self.rename_number_cell()
        #             return


abuilder = Gtk.Builder()
abuilder.add_from_file("Interfeice.glade")
abuilder.connect_signals(Handler())

Window = abuilder.get_object("main_window")
Window.connect("destroy", Gtk.main_quit)

entry = abuilder.get_object("entry_insert")
entry_sabject = abuilder.get_object("entry_sabj")

notebook = abuilder.get_object("note_book")
#sWindow_now = abuilder.get_object("scrolled_window_now") #  окно прокрутки первой вкладки
#sWindow_medium = abuilder.get_object("scrolled_window_medium") #  окно прокрутки первой вкладки
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

for i, column_title in enumerate(
        ["№", "Список срочных дел", "Дата"]
):
    renderer = Gtk.CellRendererText()
    column = Gtk.TreeViewColumn(column_title, renderer, text=i)
    tree_now.append_column(column)

for i, column_title in enumerate(
        ["№", "Список среднесрочных дел", "Дата"]
):
    renderer = Gtk.CellRendererText()
    column = Gtk.TreeViewColumn(column_title, renderer, text=i)
    tree_medium.append_column(column)

for i, column_title in enumerate(
        ["№", "Список перспективных дел", "Дата"]
):
    renderer = Gtk.CellRendererText()
    column = Gtk.TreeViewColumn(column_title, renderer, text=i)
    tree_perspective.append_column(column)

# select = tree_now.get_selection()  # выбор таблицы
# select.connect("changed", on_tree_selection_changed)  # подключение сигнала выбранной строки


#sWindow_now.add(tree_now)

Window.show_all()
#whatis(notebook)
if __name__ == '__main__':
    commands.CreateBookmarksTableCommand().execute('bookmarks')  # инициализация БД
    Option('List bookmarks by date', commands.ListBookmarksCommand()).choose('bookmarks')
    notebook.next_page()
    Option('List bookmarks by date', commands.ListBookmarksCommand()).choose('bookmarks_medium')
    notebook.next_page()
    Option('List bookmarks by date', commands.ListBookmarksCommand()).choose('bookmarks_perspective')
    notebook.set_current_page(0)
    entry_sabject.set_text("Таблица загружена")
    Gtk.main()
