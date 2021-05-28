from abc import ABC, abstractmethod

from database import DatabaseManager

name_table = ['bookmarks', 'bookmarks_medium', 'bookmarks_perspective']


class PersistenceLayer(ABC):  # <1>
    @abstractmethod
    def create(self, table_name, data):  # <2>
        raise NotImplementedError('Команды должны реализовывать метод create')

    @abstractmethod
    def list(self, table_name, order_by=None):
        raise NotImplementedError('Команды должны реализовывать метод list')

    @abstractmethod
    def edit(self, table_name, bookmark_id, bookmark_data):
        raise NotImplementedError('Команды должны реализовывать метод edit')

    @abstractmethod
    def delete(self, table_name, bookmark_id):
        raise NotImplementedError('Команды должны реализовывать метод delete')


class BookmarkDatabase(PersistenceLayer):  # <3>
    def __init__(self):
        for name in name_table:
            self.table_name = name  # <4>
            self.db = DatabaseManager('bookmarks.db')

            self.db.create_table(self.table_name, {
                'id': 'integer primary key autoincrement',
                'title': 'text not null',
                # 'url': 'text not null',
                # 'notes': 'text',
                'date_added': 'text not null',
            })

    def create(self, table_name, bookmark_data):  # <5>
        self.db.add(table_name, bookmark_data)

    def list(self, table_name, order_by=None):
        return self.db.select(table_name, order_by=order_by).fetchall()

    def edit(self, table_name, bookmark_id, bookmark_data):
        # self.db.update(table_name, {'id': bookmark_id}, bookmark_data)
        self.db.update(table_name, {'id': bookmark_id}, bookmark_data)

    def delete(self, table_name, bookmark_id):
        self.db.delete(table_name, {'id': bookmark_id})
        # self.db.delete(table_name, bookmark_id)
