from modules.modules import create_telephone_book
from modules.modules import create_record
from modules.modules import show_record
from modules.modules import fix_record
from modules.modules import delete_record
from modules.modules import show_all_records
from modules.modules import exit_
from modules.modules import create_telephone_book
from modules.modules import cheak_exist_telephone_book
from modules.modules import cheak_structure
from modules.modules import delete_telephone_book


from pathlib import Path
import json 
import pandas as pd


def controler() -> tuple:

    menu_type = 'lower'

    print("--------------Главное меню---------------")

    menu = {
        '1':('Создать контакт', create_record),
        '2':('Найти контакт', show_record),
        '3':('Изменить контакт', fix_record),
        '4':('Удалить контакт', delete_record),
        '5':('Показать список контактов', show_all_records),
        '6':('ВЫХОД', exit_)
    }  

    for key, item in menu.items():

        print(key, item[0])

    print("-----------------------------------------")
    print()
    choise = input('''Выберите пункт меню: ''')
    
    if choise in menu.keys():

        result_tuple = choise, menu_type, menu[choise][1],

        return result_tuple
    
    else:
        print('''
              ---------------------------------------
              Нет такой функции. Попробуйте еще раз!
              ---------------------------------------
              ''')
        return controler()


current_path = Path.cwd
target_dir = Path('list_dir')
target_file_path = Path(f'{target_dir}//list.json')


if cheak_exist_telephone_book(target_dir, target_file_path):

    cheak = cheak_structure(target_file_path)

    if cheak[0]:


        print(f'''Справочник уже создан!
            
            Структура справочника:

            {cheak[1]}

            ''')
        print('')

    else:
        print(f'''Справочник уже создан! Но структура не соответсвует требованиям.
            
            Структура справочника:

            {cheak[1]}

            ''')
        print('')
        print('Удалить и пересоздать Y/N?')
        delete_and_create = input()

        if delete_and_create == 'Y':

            if delete_telephone_book(current_path, target_dir)[0] == True:
                
                if create_telephone_book(target_dir, target_file_path) [0] == True:

                    print('Справочник успешно создан. Структура верная!')


        elif delete_and_create == 'N':
            print('Структура справочника не соответсвует. Перед началом работы необходимо удалить имеющийся справочник.')
            exit()
            
else:
    print('Справочник не найден.')
    print('Создать справочник Y/N?')
    create = input()

    if create == 'Y':

        if create_telephone_book(target_dir, target_file_path) [0] == True:
                    
                    pass
        else:
            # Добавить логику 
            pass

    elif create == 'N':
        print('''
              ---------------------------------------
              Вы вышли из программы!
              ---------------------------------------
              ''')
        exit()
    else:
        print('''
              ---------------------------------------
              Вы ввели неверное значение и это привело к закрытию программы!
              Попробуйте перезапустить программу и сделать выбор снова.
              ---------------------------------------
              ''')
        exit()



while True:
    
    requests_func = controler()

    print(requests_func)

    if requests_func[1] == 'lower':
        sub_func = requests_func[2](target_file_path)

        print(sub_func)
        if sub_func[1] == 'top':
            continue
    


