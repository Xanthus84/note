#!/usr/bin/env python

import os
from collections import OrderedDict

import commands
#whatis = lambda obj: print(type(obj), "\n\t" + "\n\t".join(dir(obj)))

def print_bookmarks(bookmarks):
    for bookmark in bookmarks:
        print('\t'.join(
            str(field) if field else ''
            for field in bookmark
        ))


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


def clear_screen():
    clear = 'cls' if os.name == 'nt' else 'clear'
    os.system(clear)


def print_options(options):
    for shortcut, option in options.items():
        print(f'({shortcut}) {option}')
    print()


def option_choice_is_valid(choice, options):  # функция проверки правильности выбора пользователя
    return choice in options or choice.upper() in options  # <1> вариант является допустимым, если буква совпадает с
    # одним из ключей в словаре option


def get_option_choice(options):
    choice = input('Choose an option: ')  # <2> получает от пользователя первоначальный вариант
    while not option_choice_is_valid(choice, options):  # <3> пока вариант пользователя остается не допустимым,
        # продолжать предлагать ему ввести данные
        print('Invalid choice')
        choice = input('Choose an option: ')
    return options[choice.upper()]  # <4> возвращает совпадающий вариант, когда сделан правильный выбор


def get_user_input(label, required=True):  # <1> общая функция, которая предлагает пользователя ввести данные
    value = input(f'{label}: ') or None  # <2> получает первоначальный ввод от пользователя
    while required and not value:  # <3> при необходимости продолжает предлагать ввод до тех пор, пока входные данные
        # остаются пустыми
        value = input(f'{label}: ') or None
    return value


def get_new_bookmark_data():  # <4> функция, которая получает необходимые данные для добавления новой закладки
    return {
        'title': get_user_input('Title'),
        'url': get_user_input('URL'),
        'notes': get_user_input('Notes', required=False),  # <5> примечания для закладки не являются обязательными,
        # поэтому не продолжает предлагать их ввести
    }


def get_bookmark_id_for_deletion():  # <6> получает необходимую информацию для удаления закладки
    return get_user_input('Enter a bookmark ID to delete')


def loop():  # <1> всё, что происходит для каждой итерации цикла меню -> опция -> результат - уходит сюда
    clear_screen()

    options = OrderedDict({
        'A': Option('Add a bookmark', commands.AddBookmarkCommand(), prep_call=get_new_bookmark_data),
        'B': Option('List bookmarks by date', commands.ListBookmarksCommand()),
        'T': Option('List bookmarks by title', commands.ListBookmarksCommand(order_by='title')),
        'D': Option('Delete a bookmark', commands.DeleteBookmarkCommand(), prep_call=get_bookmark_id_for_deletion),
        'Q': Option('Quit', commands.QuitCommand()),
    })
    print_options(options)

    chosen_option = get_option_choice(options)
    clear_screen()
    chosen_option.choose()

    _ = input('Press ENTER to return to menu')  # <2> предлагает пользователю нажать ENTER и просматривает результат
    # перед продолжением работы (_ - означает "неиспользуемое значение")

#whatis(tuple)
if __name__ == '__main__':
    commands.CreateBookmarksTableCommand().execute()  # инициализация БД

    while True:  # <3> опрос пользователя в цикле, выход из цикла по 'Q'
        loop()


def for_listings_only():
    options = {
        'A': Option('Add a bookmark', commands.AddBookmarkCommand()),
        'B': Option('List bookmarks by date', commands.ListBookmarksCommand()),
        'T': Option('List bookmarks by title', commands.ListBookmarksCommand(order_by='title')),
        'D': Option('Delete a bookmark', commands.DeleteBookmarkCommand()),
        'Q': Option('Quit', commands.QuitCommand()),
    }
    print_options(options)
