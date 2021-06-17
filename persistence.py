from abc import ABC, abstractmethod

from database import DatabaseManager

name_table = ['bookmarks', 'bookmarks_medium', 'bookmarks_perspective']


class PersistenceLayer(ABC):  #
    @abstractmethod
    def create_table(self, table_name):  # абстрактный метод создания таблицы после ее удаления методом drop
        raise NotImplementedError('Команды должны реализовывать метод create_table')

    @abstractmethod
    def create(self, table_name, data):  # абстрактный метод создания новой заметки
        raise NotImplementedError('Команды должны реализовывать метод create')

    @abstractmethod
    def list(self, table_name, order_by=None):  # абстрактный метод вывода списка заметок
        raise NotImplementedError('Команды должны реализовывать метод list')

    @abstractmethod
    def edit(self, table_name, bookmark_id, bookmark_data):  # абстрактный метод редактирования заметки
        raise NotImplementedError('Команды должны реализовывать метод edit')

    @abstractmethod
    def delete(self, table_name, bookmark_id):  # абстрактный метод удаления заметки
        raise NotImplementedError('Команды должны реализовывать метод delete')

    @abstractmethod
    def drop(self, table_name):  # абстрактный метод удаления таблицы
        raise NotImplementedError('Команды должны реализовывать метод drop')


class BookmarkDatabase(PersistenceLayer):  # класс команд по работе с функционалом бд
    def __init__(self):  # инициализация БД
        for name in name_table:
            self.table_name = name  #
            self.db = DatabaseManager('bookmarks.db')

            self.db.create_table(self.table_name, {
                'id': 'integer primary key autoincrement',
                'title': 'text not null',
                # 'url': 'text not null',
                # 'notes': 'text',
                'date_added': 'text not null',
            })

    def create_table(self, table_name):  # создание таблицы после ее удаления методом drop
        self.db.create_table(table_name, {
            'id': 'integer primary key autoincrement',
            'title': 'text not null',
            # 'url': 'text not null',
            # 'notes': 'text',
            'date_added': 'text not null',
        })

    def create(self, table_name, bookmark_data):  # создание новой заметки
        self.db.add(table_name, bookmark_data)

    def list(self, table_name, order_by=None):  # вывод списка заметок
        return self.db.select(table_name, order_by=order_by).fetchall()

    def edit(self, table_name, bookmark_id, bookmark_data):  # редактирование заметки
        # self.db.update(table_name, {'id': bookmark_id}, bookmark_data)
        self.db.update(table_name, {'id': bookmark_id}, bookmark_data)

    def delete(self, table_name, bookmark_id):  # удаление заметки
        self.db.delete(table_name, {'id': bookmark_id})
        # self.db.delete(table_name, bookmark_id)

    def drop(self, table_name):  # удаление таблицы
        self.db.drop_table(table_name)
        # self.db.delete(table_name, bookmark_id)
