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


# def on_tree_selection_changed(selection):  # функция показывает значение в выделенном пользователем столбце и строке
#     model, treeiter = selection.get_selected()
#     if treeiter is not None:
#         print("You selected", model[treeiter][1])


class Handler:
    def get_note_clicked_cb(self, button):
        software_list = [len(lStore_now) + 1, entry.get_text()]
        # for row in lStore_now:  # цикл вывода на печать всех значений списка
        #     print(row[:])
        lStore_now.append(list(software_list))

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
        # lStore_now.clear()
        selection = tree_now.get_selection()
        num = selection.count_selected_rows()
        if num > 0:
            for i in range(len(lStore_now)):
                path = Gtk.TreePath(i)
                treeiter = lStore_now.get_iter(path)
                if selection.iter_is_selected(treeiter) == True:
                    lStore_now.remove(treeiter)
                    self.rename_number_cell()
                    return


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

lStore_now = Gtk.ListStore(int, str)
for software_ref in software_list:
    lStore_now.append(list(software_ref))

tree_now = Gtk.TreeView(model=lStore_now)
for i, column_title in enumerate(
        ["№", "Список срочных дел"]
):
    renderer = Gtk.CellRendererText()
    column = Gtk.TreeViewColumn(column_title, renderer, text=i)
    tree_now.append_column(column)

# select = tree_now.get_selection()  # выбор таблицы
# select.connect("changed", on_tree_selection_changed)  # подключение сигнала выбранной строки

sWindow_now.add(tree_now)

Window.show_all()
# whatis(tree_now.get_mode)
Gtk.main()
