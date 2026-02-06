import json
import pandas as pd
from pathlib import Path
from typing import Dict
from functools import wraps
from dataclasses import dataclass
from typing import Optional, Any

print(Path.cwd()/'app'/'data'/'menu_message.json')




class View:
    """
    Класс View отвечает за отображение пользовательского интерфейса
    и обработку пользовательского ввода в консольном приложении.

    Класс управляет:
    - навигацией по меню;
    - выводом сообщений, ошибок и данных;
    - сбором пользовательского ввода;
    - хранением промежуточного состояния через DataClass.
    """

    def __init__(self):
        """
        Инициализирует объект View.

        Проверяет существование файла с сообщениями меню,
        загружает его содержимое и создаёт объект состояния DataClass.
        """
        self.__target_file = Path.cwd() / 'app' / 'data' / 'menu_message.json'

        if not Path.exists(self.__target_file):
            raise FileNotFoundError('Путь не существует.')

        self.__menu_set = self._load_message_set()
        self.data = self.DataClass()

    @dataclass
    class DataClass:
        """
        Класс-контейнер для хранения состояния View.

        Используется для передачи данных между слоями приложения.
        """

        current_navigation: str = 'menu'
        next_execute_function: str = None
        user_responce: int = None
        message: Optional[str] = None
        error_message: Optional[str] = None
        data: Any = None

    @staticmethod
    def output_deco(type: str = None):
        """
        Декоратор для форматированного вывода заголовков интерфейса.

        :param type: тип представления (menu, error, message и т.д.)
        :type type: str
        :return: декоратор
        """
        TITLES = {
            'menu': 'Введите номер действия.',
            'message': 'СООБЩЕНИЕ!',
            'error': 'ОШИБКА!',
            'del_cocntact': 'Введите номер контакта в формате +7XXXXXXXXXX.',
            'show_contacts': 'КОНТАКТЫ.',
            'search_contact': 'Введите номер поля для поиска.',
            'create_contact': 'Введите данные нового контата.',
            'info': 'Информационное сообщение.',
            'change_contact': 'Введите номер поля для изменения.',
            'choose_contact': 'Введите номер телефона контакта для изменения.',
            'input_data': 'Введите данные.',
        }

        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                title = TITLES.get(type)
                print('-' * 57)
                if title:
                    print(f'{title:^57}')
                    print('-' * 57)
                    result = func(self, *args, **kwargs)
                    print('-' * 57)
                    print()
                return result

            return wrapper

        return decorator

    @output_deco('menu')
    def main_navigation_view(self) -> DataClass:
        """
        Основное меню навигации.

        Запрашивает у пользователя пункт меню и сохраняет выбор.
        """
        responce, menu = self._create_navigation()
        count_ = len(menu)

        try:
            responce = int(responce)
        except Exception:
            self.data.error_message = (
                'Вы ввели некоректное значение. Попробуйте еще раз:)'
            )
            return self.data

        if responce in range(1, count_ + 1):
            self.data.next_execute_function = menu[str(responce)][1]
            self.data.user_responce = responce
            return self.data

        self.data.error_message = (
            'Вы ввели некоректное значение. Попробуйте еще раз:)'
        )
        return self.data

    @output_deco('info')
    def info_view(self, massage: str = 'NO INFO') -> DataClass:
        """
        Отображает информационное сообщение.
        """
        print(massage)
        return self.data

    @output_deco('message')
    def message_view(self, massage: str = 'NO INFO') -> DataClass:
        """
        Отображает сообщение и очищает состояние сообщения.
        """
        print(massage)
        self.data.message = None
        return self.data

    @output_deco('error')
    def error_view(self, error_message: str = 'UNDEFINE ERROR') -> DataClass:
        """
        Отображает сообщение об ошибке и очищает состояние ошибки.
        """
        print(error_message)
        self.data.error_message = None
        return self.data

    @output_deco('show_contacts')
    def show_contacts_view(self, data: pd.DataFrame = None) -> DataClass:
        """
        Отображает список контактов.
        """
        if data.empty:
            self.data.message = (
                'Такого контакта не существует. Попробуйте еще раз!'
            )
            return self.data

        print(data)
        return self.data

    @output_deco('del_cocntact')
    def del_cocntact_view(self) -> DataClass:
        """
        Запрашивает номер телефона для удаления контакта.
        """
        phone = input('phone: ')
        self.data.data = phone
        return self.data

    @output_deco('search_contact')
    def search_contact_view(self) -> DataClass:
        """
        Представление для поиска контакта по выбранному полю.
        """
        responce, menu = self._create_navigation()
        count_ = len(menu)

        try:
            responce = int(responce)
        except Exception:
            self.data.error_message = (
                'Вы ввели некоректное значение. Попробуйте еще раз:)'
            )
            return self.data

        if responce in range(1, count_ + 1):
            self.data.data = {'field': menu[str(responce)][1]}
            self.data.user_responce = responce

            if 'Back' in self.data.data.values():
                self.clean_object()
                return self.data

            value = input(f"Введите {self.data.data['field']}: ")
            self.data.data['contact'] = value
            return self.data

        self.data.error_message = (
            'Вы ввели некоректное значение. Попробуйте еще раз:)'
        )
        return self.data

    @output_deco('choose_contact')
    def choose_contact_view(self) -> DataClass:
        """
        Запрашивает номер телефона контакта для изменения.
        """
        row = input('Номер телефона: ')
        self.data.data = {'field': 'phone', 'contact': row}
        return self.data.data

    @output_deco('change_contact')
    def change_contact_view(self) -> DataClass:
        """
        Представление для изменения данных контакта.
        """
        responce, menu = self._create_navigation()
        count_ = len(menu)

        try:
            responce = int(responce)
        except Exception:
            self.data.error_message = (
                'Вы ввели некоректное значение. Попробуйте еще раз:)'
            )
            return self.data

        if responce in range(1, count_ + 1):
            self.data.user_responce = responce

            if menu[str(responce)][1] == 'Back':
                self.clean_object()
                return self.data

            if menu[str(responce)][1] == 'all_fields':
                self.data.data = {}
                self.input_data_view()
                return self.data

            value = input(f"Введите {menu[str(responce)][1]}: ")
            self.data.data = {menu[str(responce)][1]: value}
            return self.data

        self.data.error_message = (
            'Вы ввели некоректное значение. Попробуйте еще раз:)'
        )
        return self.data

    @output_deco('create_contact')
    def create_contact_view(self) -> DataClass:
        """
        Запрашивает данные нового контакта.
        """
        name = input('name: ')
        phone = input('phone: ')
        comment = input('comment: ')
        self.data.data = {
            'name': name,
            'phone': phone,
            'comment': comment,
        }
        return self.data

    @output_deco('input_data')
    def input_data_view(self) -> DataClass:
        """
        Универсальный ввод данных контакта.
        """
        name = input('name: ')
        phone = input('phone: ')
        comment = input('comment: ')
        self.data.data = {
            'name': name,
            'phone': phone,
            'comment': comment,
        }
        return self.data

    def clean_object(self) -> DataClass:
        """
        Сбрасывает состояние View к значениям по умолчанию.
        """
        self.data = self.DataClass()
        return self.data

    def _create_navigation(self):
        """
        Формирует меню навигации и запрашивает ввод пользователя.
        """
        try:
            menu = self.__menu_set.get(self.data.current_navigation)
        except ValueError as error:
            raise error

        for key, item in menu.items():
            print(key, item[0])

        user_input = input('Номер: ')
        return user_input, menu

    def _load_message_set(self) -> Dict:
        """
        Загружает файл сообщений меню.
        """
        try:
            with open(self.__target_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print('Файл не существует.')

    def __repr__(self):
        """
        Официальное строковое представление объекта.
        """
        pass

    def __str__(self):
        """
        Возвращает человекочитаемое строковое представление объекта.
        """
        return (
            f'View(target_path: {self.__target_file} '
            f'menu_set:{self.__menu_set})'
        )
