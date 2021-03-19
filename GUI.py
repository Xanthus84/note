import gi
from gi.overrides.Gtk import TextBuffer
import os
from collections import OrderedDict

import commands
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

whatis = lambda obj: print(type(obj), "\n\t" + "\n\t".join(dir(obj)))

software_list = [
    [1, "C++"],
    [2, "Java"],
    [3, "Python"],
    [4, "Java"],
    [5, "C++"],
    [6, "C++"],
    [7, "Python"],
    [8, "C"],
    [9, "C"],
    [10, "C"],
    [11, "Java"],
]

# def print_bookmarks(bookmarks): #  вывод таблицы в командную строку
#     for bookmark in bookmarks:
#         print('\t'.join(
#             str(field) if field else ''
#             for field in bookmark
#         ))

def print_bookmarks(bookmarks): #  вывод таблицы в командную строку
        for software_ref in bookmarks:
            lStore_now.append(list(software_ref))


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
            print(message)

    def choose(self):  # <4> вызывается, когда вариант действия выбран из меню
        data = self.prep_call() if self.prep_call else None  # <5> вызывает подготовительный шаг, если он указан
        message = self.command.execute(
            data) if data else self.command.execute()  # <6> выполняет команду, переданную в данных из
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
# def get_user_input(label):  # <1> общая функция, которая предлагает пользователя ввести данные
#     if label in name_note_dict:
#         value = name_note_dict(label)  # <2> получает первоначальный ввод от пользователя
#     return value
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
        'title': 'Заметка1',
        'url': 'Address',
        'notes': 'note1',  # <5> примечания для закладки не являются обязательными,
        # поэтому не продолжает предлагать их ввести
    }


def get_bookmark_id_for_deletion():  # <6> получает необходимую информацию для удаления закладки
    selection = tree_now.get_selection()
    num = selection.count_selected_rows()
    if num > 0:
        for i in range(len(lStore_now)):
            path = Gtk.TreePath(i)
            treeiter = lStore_now.get_iter(path)
            if selection.iter_is_selected(treeiter) == True:
                print(str(lStore_now.get_value(treeiter, 0)))
                return str(lStore_now.get_value(treeiter, 0))
    else:
        return '0'


class Handler:
    def get_note_clicked_cb(self, button):
        Option('Add a bookmark', commands.AddBookmarkCommand(), prep_call=get_new_bookmark_data).choose()
        lStore_now.clear()
        Option('List bookmarks by date', commands.ListBookmarksCommand()).choose()
        # software_list = [len(lStore_now) + 1, entry.get_text()]
        # # for row in lStore_now:  # цикл вывода на печать всех значений списка
        # #     print(row[:])
        # lStore_now.append(list(software_list))

    def change_note_clicked_cb(self, button):
        selection = tree_now.get_selection()  # выбор таблицы
        num = selection.count_selected_rows()  # проверка, выделена ли хотя бы одна строка
        if num > 0:
            if not entry.get_text() == '':
                for i in range(len(lStore_now)):  # цикл по значениям списка
                    path = Gtk.TreePath(i)  # перебор строк с присвоением в path
                    treeiter = lStore_now.get_iter(path)  # получение iter, соответствующее path
                    if selection.iter_is_selected(treeiter) == True:  # проверка условия, выделена ли строка
                        # print(lStore_now.get_value(treeiter, 1)) # получить значение первого столбца по заданной строке
                        lStore_now.set_value(treeiter, 1, entry.get_text())  # изменяет значение первого столбца в
                        # заданной строке тестом из поля entry
                        return

    def rename_number_cell(self):
        for i in range(len(lStore_now)):  # цикл по значениям списка
            path = Gtk.TreePath(i)  # перебор строк с присвоением в path
            treeiter = lStore_now.get_iter(path)  # получение iter, соответствующее path
            lStore_now.set_value(treeiter, 0, i+1)  # изменяет значение первого столбца в
                # заданной строке тестом из поля entry

    def delete_note_clicked_cb(self, button):
        Option('Delete a bookmark', commands.DeleteBookmarkCommand(), prep_call=get_bookmark_id_for_deletion).choose()
        lStore_now.clear()
        Option('List bookmarks by date', commands.ListBookmarksCommand()).choose()
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

sWindow_now = abuilder.get_object("scrolled_window_now")
# text_now = abuilder.get_object("text_now")
# textbuffer = text_now.get_buffer()
# textbuffer.set_text('123')

lStore_now = Gtk.ListStore(int, str, str, str, str)

Option('List bookmarks by date', commands.ListBookmarksCommand()).choose()

tree_now = Gtk.TreeView(model=lStore_now)
for i, column_title in enumerate(
        ["№", "title", "url", "notes", "date"]
):
    renderer = Gtk.CellRendererText()
    column = Gtk.TreeViewColumn(column_title, renderer, text=i)
    tree_now.append_column(column)

# select = tree_now.get_selection()  # выбор таблицы
# select.connect("changed", on_tree_selection_changed)  # подключение сигнала выбранной строки



sWindow_now.add(tree_now)

Window.show_all()
#whatis(Gtk)
if __name__ == '__main__':
    Gtk.main()
    commands.CreateBookmarksTableCommand().execute()  # инициализация БД