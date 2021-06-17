# import sys
from abc import ABC, abstractmethod
from datetime import datetime

from persistence import BookmarkDatabase

persistence = BookmarkDatabase()  # <1> открывает БД, если таковой нет, то создает её в том же каталоге


class Command(ABC):
    @abstractmethod
    def execute(self, name, data, note):
        raise NotImplementedError('Команды должны реализовывать метод execute')


class CreateTableBookmarkCommand(Command):  # команда добавления закладки
    def execute(self, name, data=None, note=None):
        persistence.create_table(name)  #
        return True, None  #


class AddBookmarkCommand(Command):  # команда добавления закладки
    def execute(self, name, data, note=None):
        data['date_added'] = datetime.today().strftime(
            '%d.%m.%Y')  # .isoformat()  # добавляет текущую дату и время при добавлении записи
        persistence.create(name, data)  #
        return True, None  #


class ListBookmarksCommand(Command):  # команда для вызова на экран списка существующих закладок
    def __init__(self, order_by='date_added'):  #
        self.order_by = order_by

    def execute(self, name, data=None, note=None):
        return True, persistence.list(name, order_by=self.order_by)  #


class DeleteBookmarkCommand(Command):  # команда для удаления закладок
    def execute(self, name, data, note=None):
        persistence.delete(name, data)  # delete принимает словарь имен столбцов и сопоставляет пары значений
        return True, None


class UpdateBookmarkCommand(Command):  # команда для изменения закладок
    def execute(self, name, data, note):
        # persistence.edit(name, data['id'], data['update'])  # <1> update принимает словарь имен столбцов и
        # # сопоставляет пары значений
        persistence.edit(name, data, note)  # update принимает словарь имен столбцов и
        # сопоставляет пары значений
        return True, None


class DropBookmarkCommand(Command):  # команда для удаления таблицы
    def execute(self, name, data=None, note=None):
        persistence.drop(name)  # drop принимает словарь имен столбцов и сопоставляет пары значений
        return True, None


# class ResetIdBookmarkCommand: # команда для сброса автоинкремента
#     def execute(self, name):
#         db.reset_id(name) # <1> reset_id принимает словарь имен столбцов и сопоставляет пары значений
#         return 'Нумерация обновлена!'
# class QuitCommand:
#     def execute(self):
#         sys.exit()  # <1> приводит к выходу из программы
