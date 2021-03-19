import sys
from datetime import datetime

from database import DatabaseManager

db = DatabaseManager('bookmarks.db')  # <1> открывает БД, если таковой нет, то создает её в том же каталоге


class CreateBookmarksTableCommand: # команда для создания таблицы в БД
    def execute(self):  # <2> команда для создания таблицы с определенными заголовками при запуске приложения
        db.create_table('bookmarks', {  # <3> создает таблица используя функцию create_table
            'id': 'integer primary key autoincrement', # id каждой записи автоматически наращивается по мере добавления записей
            'title': 'text not null', # not null требует, чтобы столбец был заполнен значениями
            # 'url': 'text not null',
            # 'notes': 'text',
            'date_added': 'text not null',
        })

class AddBookmarkCommand: # команда добавления закладки
    def execute(self, data):
        data['date_added'] = datetime.today().strftime('%d.%m.%Y')  #.isoformat()  # <1> добавляет текущую дату и время при добавлении записи
        db.add('bookmarks', data)  # <2>
        return 'Заметка загружена в БД!'  # <3>


class ListBookmarksCommand: # команда для вызова на экран списка существующих закладок
    def __init__(self, order_by='date_added'):  # <1>
        self.order_by = order_by

    def execute(self):
        return db.select('bookmarks', order_by=self.order_by).fetchall()  # <2>


class DeleteBookmarkCommand: # команда для удаления закладок
    def execute(self, data):
        db.delete('bookmarks', {'id': data})  # <1> delete принимает словарь имен столбцов и сопоставляет пары значений
        return 'Заметка удалена!'

class UpdateBookmarkCommand: # команда для удаления закладок
    def execute(self, data, note):
        db.update('bookmarks', {'id': data}, note)  # <1> delete принимает словарь имен столбцов и сопоставляет пары значений
        return 'Заметка изменена!'

# class QuitCommand:
#     def execute(self):
#         sys.exit()  # <1> приводит к выходу из программы
