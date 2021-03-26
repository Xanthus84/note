import sqlite3

#whatis = lambda obj: print(type(obj), "\n\t" + "\n\t".join(dir(obj)))

class DatabaseManager:
    def __init__(self, database_filename):
        self.connection = sqlite3.connect(database_filename)  # <1> Создает и сохраняет соединение с БД для последующего использования

    def __del__(self):
        self.connection.close()  # <2> Закрывает соединение когда дело сделано

    def _execute(self, statement, values=None):  # <1> values для плэйсхолдера, для защиты функции от спама
        with self.connection:  #  создает контекст транзакции БД
            cursor = self.connection.cursor()  # создает курсор
            cursor.execute(statement, values or [])  # <2> использует курсор для выполнения инструкций
            return cursor  #  возвращает курсор с сохраненным результатом

    def create_table(self, table_name, columns):
        columns_with_types = [  # <1>  конструирует определения столбцов с их типами и ограничениями
            f'{column_name} {data_type}'
            for column_name, data_type in columns.items()
        ]
        self._execute(  # <2> конструирует полную инструкцию создания таблицы и выполняет её
            f'''
            CREATE TABLE IF NOT EXISTS {table_name}
            ({', '.join(columns_with_types)});
            '''
        )

    def drop_table(self, table_name):
        self._execute(f'DROP TABLE {table_name};')

    def add(self, table_name, data): # добавление записи в таблицу БД SQlite
        placeholders = ', '.join('?' * len(data))
        column_names = ', '.join(data.keys())  # <1> ключами являются имена столбцов
        column_values = tuple(data.values())  # <2> .values() возвращает объект dict_values, но execute требует список или картеж

        self._execute(
            f'''
            INSERT INTO {table_name}
            ({column_names})
            VALUES ({placeholders});
            ''',
            column_values,  # <3> передает необязательный аргумент values в execute
        )

    def delete(self, table_name, criteria):  # <1> критерий позволяет удалять только выбранные пользователем данные
        placeholders = [f'{column} = ?' for column in criteria.keys()]
        delete_criteria = ' AND '.join(placeholders)
        self._execute(
            f'''
            DELETE FROM {table_name}
            WHERE {delete_criteria};
            ''',
            tuple(criteria.values()),  # <2> использует аргумент values метода _execute в качестве значений на удаление
        )

    def select(self, table_name, criteria=None, order_by=None): # метод отбора данных из таблиц SQL
        criteria = criteria or {}  # <1> по умолчанию критерии могут быть пустыми, потому что нормально, если в таблице отбираются все записи

        query = f'SELECT * FROM {table_name}'

        if criteria:  # <2> конструирует предикатное условие WHERE для ограничения результов
            placeholders = [f'{column} = ?' for column in criteria.keys()]
            select_criteria = ' AND '.join(placeholders)
            query += f' WHERE {select_criteria}'

        if order_by:  # <3> Конструирует предикатное условие ORDER BY для сортировки результатов
            query += f' ORDER BY {order_by}'

        return self._execute(  # <4> возврат значения из _execute для прокручивания его в цикле
            query,
            tuple(criteria.values()),
        )

    def update(self, table_name, criteria, note):
            placeholders = [f'{column} = ?' for column in criteria.keys()]
            update_criteria = ' AND '.join(placeholders)
            self._execute(
                f'''
                UPDATE {table_name}
                SET title = "{note}"
                WHERE {update_criteria};
                ''',
                tuple(criteria.values()),
            )
    # def reset_id(self, table_name):
    #     self._execute(
    #         f'''
    #         UPDATE SQLITE_SEQUENCE
    #         SET seq = 0
    #         WHERE name = "{table_name}";
    #         '''
    #     )

#whatis(tuple)