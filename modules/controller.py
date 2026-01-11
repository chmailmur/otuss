from modules.model import create_telephone_book
from modules.model import exit_
from modules.model import create_telephone_book
from modules.model import cheak_exist_telephone_book
from modules.model import cheak_structure
from modules.model import delete_telephone_book



from pathlib import Path
import json 
import pandas as pd



current_path = Path.cwd
target_dir = Path('list_dir')
target_file_path = Path(f'{target_dir}//list.json')

def main():

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


    


