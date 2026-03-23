import shutil
import json
from typing import Dict
import pandas as pd
from pathlib import Path
from functools import wraps

class PhoneBook:
    """
    Класс для работы с телефонной книгой.

    Отвечает за:
    - создание файла телефонной книги;
    - проверку существования и структуры файла;
    - CRUD-операции с контактами;
    - предоставление интерфейса методов через словарь функций.
    """

    def __init__(self, path:Path):
        """
        Инициализирует путь к файлу телефонной книги и проверяет его состояние.

        При необходимости создаёт файл с дефолтной структурой.
        Также формирует словарь доступных пользовательских функций.
        """
        self.phone_book_path = path

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

    def _read_pb(self) -> pd.DataFrame:
        df = pd.read_csv(self.phone_book_path)
        return df 

    def _write_pb(self, data:pd.DataFrame) -> None:
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Ошибка типа данных")
        data.to_csv(self.phone_book_path, index=False)

    def show_contacts(self) -> pd.DataFrame:
        """
        Возвращает все контакты телефонной книги.

        :return: DataFrame со всеми контактами
        :rtype: pd.DataFrame
        """
        data = self._read_pb()

        if not data.empty:
            return data
        else:
            return "Справочник пуст!"
        
    def create_contact(self, data_set: Dict = None) -> bool:
        """
        Создаёт новый контакт в телефонной книге.

        :param data_set: словарь с ключами name, phone, comment
        :type data_set: Dict
        :return: True при успешном создании
        :rtype: bool
        """
        if data_set is None:
            raise ValueError("data is None")

        if not isinstance(data_set, dict):
            raise ValueError("Data type is incorrect")
        
        keys = {'name', 'phone', 'comment'}
        if not keys.issubset(data_set.keys()):
            raise ValueError('Not all fields passed')
        
        not_acceptable_value = {'','0','-', 0}
        if data_set['name'] in not_acceptable_value:
            raise AttributeError('Not acceptable name value')

        if data_set['phone'] in not_acceptable_value:
            raise AttributeError('Not acceptable phone value')

        data = self._read_pb()
        new_row = [
            {"name": data_set['name'], 
             "phone": data_set['phone'], 
             "comment": data_set['comment']}
        ]
        data = pd.concat([data, pd.DataFrame(new_row)],ignore_index=True)
        self._write_pb(data)
        
        return True

    def search_contact(self, search_dict: Dict = None) -> pd.DataFrame:
        """
        Ищет контакт по указанному полю и значению.

        :param search_dict: словарь с ключами field и contact
        :type search_dict: Dict
        :return: DataFrame с найденными контактами
        :rtype: pd.DataFrame
        """
        if search_dict is None:
            raise ValueError("data is None")

        if not isinstance(search_dict, dict):
            raise ValueError("Data type is incorrect")
        
        keys = {'field', 'contact'}
        if not keys.issubset(search_dict.keys()):
            raise ValueError('Not all fields passed')
        
        not_acceptable_value = {'','0','-', 0}
        if search_dict['contact'] in not_acceptable_value:
            raise AttributeError('Not acceptable name value')
        
        field, contact = search_dict.get('field'), search_dict.get('contact')

        if (field is not None) or (contact is not None):
            data = self._read_pb()
            data = data[data[field] == contact]
            return data

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

        data = self._read_pb()

        if 'phone' not in data.columns:
            return pd.DataFrame()

        delited_contact = data[data['phone'] == number]
        if delited_contact.empty:
            return pd.DataFrame()

        data = data[data['phone'] != number]

        self._write_pb(data)
        
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

        if not isinstance(data_new, dict):
            raise ValueError("Data type is incorrect")
        
        not_acceptable_value = {'','0','-', 0}
        if 'name' in data_new.keys():
            if data_new['name'] in not_acceptable_value:
                raise AttributeError('Not acceptable name value')
        if 'phone' in data_new.keys():
            if data_new['phone'] in not_acceptable_value:
                    raise AttributeError('Not acceptable phone value')


        data = self._read_pb()
        idx = data.index[data['phone'] == old_data['contact']][0]

        for key, val in data_new.items():
            data.at[idx, key] = val

        self._write_pb(data)
    
        return data

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

        data = self._read_pb()


        if not isinstance(data, pd.DataFrame):
            return False

        required_keys = {'name','phone','comment'}
        if required_keys.issubset(data.columns):
            return True
        else: 
            return  False

    def _create_telephone_book(self) -> bool:
        """
        Создаёт файл телефонной книги с дефолтной структурой.

        :return: True при успешном создании
        :rtype: bool
        """
        structure = {
            "name":{},
            "phone":{},
            "comment":{}
        }
        data = pd.DataFrame(structure)
        
        self._write_pb(data)

        return True

    
  