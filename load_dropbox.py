import dropbox
from dropbox.exceptions import AuthError

access_token = 'l5vm0BqLCUoAAAAAAAAAATbzoRZNo--8_042EyE3sRtyQOFmwN8DVQo4UhKE2kko'


# dbx = dropbox.Dropbox(access_token)  # наш access token
# dbx.users_get_current_account()  # проверка подключения
# whatis = lambda obj: print(type(obj), "\n\t" + "\n\t".join(dir(obj)))
# whatis(dbx)
class Dropbox:
    def __init__(self):
        self.dbx = dropbox.Dropbox(access_token)  # наш access token

    def load_to_dropbox(self, files):  # функция загрузки в дропбокс БД
        try:
            self.dbx.users_get_current_account()
        except:
            return "Ошибка подключения!"
        with open(files, 'rb') as file:  # открываем файл в режиме чтение побайтово
            response = self.dbx.files_upload(file.read(),
                                             '/bookmarks.db',
                                             mode=dropbox.files.WriteMode.overwrite)  # загружаем файл: первый аргумент (file.read()) - какой файл; второй
            # - название, которое будет присвоено файлу уже на дропбоксе.
            return response  # возвращаем результат загрузки

    def print_url(self):
        try:
            self.dbx.users_get_current_account()
        except:
            return "Ошибка подключения!"
        # Выведет на экран url файла bookmarks.db для скачивания
        return self.dbx.files_get_temporary_link('/bookmarks.db').link

    def save_file_from_dropbox(self, files):
        try:
            self.dbx.users_get_current_account()
        except:
            return "Ошибка подключения!"
        with open(files, 'wb') as file:  # открываем файл в режиме чтение побайтово
            metadata, response = self.dbx.files_download(
                path='/bookmarks.db')  # загружаем файл: первый аргумент (file.read()) - какой файл; второй
            file.write(response.content)
            return response  # возвращаем результат загрузки
