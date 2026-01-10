from pathlib import Path

from modules.modules import create_catalog
from modules.modules import create_record
from modules.modules import show_record
from modules.modules import fix_record
from modules.modules import delete_record
from modules.modules import show_all_records
from modules.modules import exit_
from modules.modules import create_telephone_book
from modules.modules import cheak_telephone_book
from modules.modules import cheak_structure



import json 



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




if cheak_telephone_book(target_dir, target_file_path):

    cheak = cheak_structure(target_file_path)

    if cheak[0]:


        print(f'''Справочник уже создан!
            
            Структура справочника:

            {cheak[1]}

            ''')
        print('')

    else:
        print(f'''Справочник уже создан! Но структура не соответсвует.
            
            Структура справочника:

            {cheak[1]}

            ''')
        print('')
        print('Удалить и пересоздать Y/N?')
        delete_and_create = input()

        if delete_and_create == 'Y':

            cheak_telephone_book()
        elif delete_and_create == 'Y':
            print('Структура справочника не соответсвует. Перед началом работы необходимо удалить имеющийся справочник.')
            exit()
            
        

else:
    print('Справочник не найден.')
    print('Создать справочник Y/N?')
    create = input()

    if create == 'Y':

        cheak_telephone_book()


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
        sub_func = requests_func[2]()

        if sub_func[1] == 'top':
            continue
    


