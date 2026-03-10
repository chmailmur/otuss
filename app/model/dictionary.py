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

    def _read_pb(self) -> Dict:
        try: 
            with self.phone_book_path.open(mode='r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError as error:
            raise ValueError(f'Справочник поврежден: {error}')

    def _write_pb(self, content:Dict) -> None:
        try: 
            with self.phone_book_path.open(mode='w', encoding='utf-8') as file:
                return json.dump(content, file, indent=4, ensure_ascii=False)
        except OSError as err:
            raise OSError(f'Файл не записан: {err}')

    def show_contacts(self) -> pd.DataFrame:
        """
        Возвращает все контакты телефонной книги.

        :return: DataFrame со всеми контактами
        :rtype: pd.DataFrame
        """
        content = self._read_pb()

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

        if data_set is None:
            raise ValueError('data_set не передан!')

        req_fields = {'name', 'phone', 'comment'}
        if not req_fields.issubset(data_set.keys()):
            raise ValueError('Не все обязательные поля переданы')
        
        wrong_val = {''}
        if wrong_val.issubset(list(data_set.values())[:-1]):
            raise ValueError('Имя и телефон не могут быть пустыми строками.')

        content = self._read_pb()

        last_key = [_ for _ in content.keys()][-1]
        last_key = int(last_key) + 1
        new_key = str(last_key)

        content[new_key] = data_set

        self._write_pb(content)
        
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
            content = self._read_pb()
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

        content = self._read_pb()

        df = pd.DataFrame.from_dict(content, orient='index')

        if 'phone' not in df.columns:
            return pd.DataFrame()

        delited_contact = df[df['phone'] == number]
        if delited_contact.empty:
            return pd.DataFrame()

        df = df[df['phone'] != number]

        self._write_pb(df.to_dict(orient='index'), indent=4)
        
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

        content = self._read_pb()

        df = pd.DataFrame.from_dict(content, orient='index')
        idx = df.index[df['phone'] == old_data['contact']][0]

        for key, val in data_new.items():
            df.at[idx, key] = val

        self._write_pb(df.to_dict(orient='index'))
    
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

        content = self._read_pb()

        if not isinstance(content, dict) or not content:
            return False

        first_record = next(iter(content.values()))

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
        self._write_pb(structure)

        return True

    
  