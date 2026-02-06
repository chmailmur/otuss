import shutil
import json
from typing import Dict
import pandas as pd
from pathlib import Path
from functools import wraps

print(Path.cwd()/'app'/'data'/'phone_book.json')

class PhoneBook:
    """
    Класс для работы с телефонной книгой.

    Отвечает за:
    - создание файла телефонной книги;
    - проверку существования и структуры файла;
    - CRUD-операции с контактами;
    - предоставление интерфейса методов через словарь функций.
    """

    def __init__(self):
        """
        Инициализирует путь к файлу телефонной книги и проверяет его состояние.

        При необходимости создаёт файл с дефолтной структурой.
        Также формирует словарь доступных пользовательских функций.
        """
        self.phone_book_path = Path.cwd() / 'app' / 'data' / 'phone_book.json'

        if self._check_exists_phone_book():
            self.exists = True
            if self._check_structure():
                self.stucture_matches = True
            else:
                if self._create_telephone_book():
                    self.exists = True
        else:
            if self._create_telephone_book():
                self.exists = True

        self.functions = {
            'show_contacts': self.show_contacts,
            'del_cocntact': self.del_cocntact,
            'search_contact': self.search_contact,
            'create_contact': self.create_contact,
            'change_contact': self.change_contact,
        }

    def show_contacts(self) -> pd.DataFrame:
        """
        Возвращает все контакты телефонной книги.

        :return: DataFrame со всеми контактами
        :rtype: pd.DataFrame
        """
        try:
            with self.phone_book_path.open(mode='r', encoding='utf-8') as file:
                content = json.load(file)
        except FileNotFoundError:
            raise

        df = pd.DataFrame.from_dict(content, orient='index')
        return df

    def create_contact(self, data_set: Dict = None) -> bool:
        """
        Создаёт новый контакт в телефонной книге.

        :param data_set: словарь с ключами name, phone, comment
        :type data_set: Dict
        :return: True при успешном создании
        :rtype: bool
        """
        try:
            with self.phone_book_path.open(mode='r', encoding='utf-8') as file:
                content = json.load(file)
        except FileNotFoundError:
            raise

        last_key = [_ for _ in content.keys()][-1]
        last_key = int(last_key) + 1
        last_key = str(f'{last_key}')

        if (
            data_set.get('name') is not None
            and data_set.get('phone') is not None
            and data_set.get('comment') is not None
        ):
            content[last_key] = data_set
        else:
            raise ValueError('Не все значения аргументы переданы.')

        try:
            with self.phone_book_path.open(mode='w', encoding='utf-8') as file:
                json.dump(content, file, indent=4)
        except Exception as err:
            raise err

        return True

    def search_contact(self, search_dict: Dict = None) -> pd.DataFrame:
        """
        Ищет контакт по указанному полю и значению.

        :param search_dict: словарь с ключами field и contact
        :type search_dict: Dict
        :return: DataFrame с найденными контактами
        :rtype: pd.DataFrame
        """
        field, contact = search_dict.get('field'), search_dict.get('contact')

        if (field is not None) or (contact is not None):
            try:
                with self.phone_book_path.open(mode='r', encoding='utf-8') as file:
                    content = json.load(file)
            except FileNotFoundError:
                raise

            df = pd.DataFrame.from_dict(content, orient='index')
            df = df[df[field] == contact]
            return df

        return pd.DataFrame()

    def del_cocntact(self, number: str = None) -> pd.DataFrame:
        """
        Удаляет контакт по номеру телефона.

        :param number: номер телефона для удаления
        :type number: str
        :return: DataFrame с удалённым контактом
        :rtype: pd.DataFrame
        """
        if number is None:
            return pd.DataFrame()

        try:
            with self.phone_book_path.open(mode='r', encoding='utf-8') as file:
                content = json.load(file)
        except FileNotFoundError:
            raise

        df = pd.DataFrame.from_dict(content, orient='index')

        if 'phone' not in df.columns:
            return pd.DataFrame()

        delited_contact = df[df['phone'] == number]
        if delited_contact.empty:
            return pd.DataFrame()

        df = df[df['phone'] != number]

        try:
            with self.phone_book_path.open(mode='w', encoding='utf-8') as file:
                file.write(
                    json.dumps(df.to_dict(orient='index'), indent=4)
                )
        except Exception as err:
            raise err

        return delited_contact
    
    def change_contact(
        self,
        old_data: Dict = None,
        data_new: Dict = None,
    ) -> pd.DataFrame:
        """
        Изменяет данные существующего контакта.

        :param old_data: данные для поиска контакта
        :type old_data: Dict
        :param data_new: новые значения полей контакта
        :type data_new: Dict
        :return: DataFrame с обновлёнными данными
        :rtype: pd.DataFrame
        """
        if data_new is None:
            return pd.DataFrame()

        try:
            with self.phone_book_path.open(mode='r', encoding='utf-8') as file:
                content = json.load(file)
        except Exception:
            raise FileNotFoundError('Файл не найден.')

        df = pd.DataFrame.from_dict(content, orient='index')
        idx = df.index[df['phone'] == old_data['contact']][0]

        for key, val in data_new.items():
            df.at[idx, key] = val

        try:
            with self.phone_book_path.open(mode='w', encoding='utf-8') as file:
                file.write(
                    json.dumps(df.to_dict(orient='index'), indent=4)
                )
        except Exception as err:
            raise err

        return df

    def _check_exists_phone_book(self) -> bool:
        """
        Проверяет существование файла телефонной книги.

        :return: True если файл существует
        :rtype: bool
        """
        return self.phone_book_path.exists()

    def _check_structure(self) -> bool:
        """
        Проверяет корректность структуры файла телефонной книги.

        :return: True если структура соответствует ожиданиям
        :rtype: bool
        """
        if not self.phone_book_path.exists():
            return False

        try:
            with self.phone_book_path.open('r', encoding='utf-8') as file:
                data = json.load(file)
        except (json.JSONDecodeError, OSError):
            return False

        if not isinstance(data, dict) or not data:
            return False

        first_record = next(iter(data.values()))

        if not isinstance(first_record, dict):
            return False

        required_keys = {'name', 'phone', 'comment'}
        return required_keys.issubset(first_record.keys())

    def _create_telephone_book(self) -> bool:
        """
        Создаёт файл телефонной книги с дефолтной структурой.

        :return: True при успешном создании
        :rtype: bool
        """
        structure = {
            '0': {
                'name': 'your name',
                'phone': '+7XXXXXXXXXX',
                'comment': 'Default contact',
            }
        }

        with self.phone_book_path.open('w', encoding='utf-8') as file:
            json.dump(structure, file, indent=4, ensure_ascii=False)

        return True

    
  