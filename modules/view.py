from modules.model import create_record
from modules.model import show_record
from modules.model import fix_record
from modules.model import delete_record
from modules.model import show_all_records
from modules.model import exit_


def view_func() -> tuple:

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
        return view_func()
