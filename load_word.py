import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from docxtpl import DocxTemplate


def create_a_report(lStore_now, lStore_medium, lStore_perspective, place):
    try:
        template = DocxTemplate('load_word.docx')
    except:
        return "NO_FILE"
    table_contents1 = []
    table_contents2 = []
    table_contents3 = []
    # сохранение значений из базы данных в списки
    for i in range(2, len(lStore_now) + 2):
        path = Gtk.TreePath(i - 2)  # перебор строк с присвоением в path
        treeiter = lStore_now.get_iter(path)
        table_contents1.append({
            'index': lStore_now.get_value(treeiter, 0),
            'note': lStore_now.get_value(treeiter, 1),
            'data': lStore_now.get_value(treeiter, 2),
        })
    for i in range(2, len(lStore_medium) + 2):
        path = Gtk.TreePath(i - 2)  # перебор строк с присвоением в path
        treeiter = lStore_medium.get_iter(path)
        table_contents2.append({
            'index': lStore_medium.get_value(treeiter, 0),
            'note': lStore_medium.get_value(treeiter, 1),
            'data': lStore_medium.get_value(treeiter, 2),
        })
    for i in range(2, len(lStore_perspective) + 2):
        path = Gtk.TreePath(i - 2)  # перебор строк с присвоением в path
        treeiter = lStore_perspective.get_iter(path)
        table_contents3.append({
            'index': lStore_perspective.get_value(treeiter, 0),
            'note': lStore_perspective.get_value(treeiter, 1),
            'data': lStore_perspective.get_value(treeiter, 2),
        })
    # формирование словаря данных для подстановки
    context = {
        'table_contents1': table_contents1,
        'table_contents2': table_contents2,
        'table_contents3': table_contents3,
    }

    template.render(context)  # загрузка содержимого словаря в Word
    try:
        template.save(place + '\\ToDoIt.docx')
        return "OK"
    except:
        return "Error"
