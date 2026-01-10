from pathlib import Path
import shutil
import json


def cheak_exist_telephone_book(dir, path_file):

    if dir.is_dir() and path_file.exists():
        return True
    else:
        return False
    

    
def cheak_structure(path_file):

    with path_file.open(mode='r', encoding='utf-8') as file:

        data_list = file.read()

        data_list = json.loads(data_list)

    structure = [data_list[i].keys() for i in data_list.keys()][0]

    if len(structure) == 3 and ('name' in structure and 'phone' in structure and 'comment' in structure):

        return True, structure
    
    else:
        return False, structure



def create_telephone_book(dir, file_path):

    menu_type = 'top'
    
    stucture = {
        'row_0':{
            'name': 'your name',
            'phone': '+7XXXXXXXXXX',
            'comment': 'Defolt contact',
        }
    }     
    
    dir.mkdir(exist_ok=True)

    with file_path.open(mode='w', encoding='utf-8') as file:
        
        file.write(json.dumps(stucture, indent=4))

    print("Справочник был создан! Можно начать работу")
    
    return (True,menu_type,)



def delete_telephone_book(parrent_dir, dir):

    menu_type = 'top'

    if dir.exists():
        shutil.rmtree(dir)

    return (True,menu_type,)



def create_record(file_path):
    menu_type = 'top'

    print('Введите имя')
    name =  input()
    print('Введите номер')
    phone =  input()
    print('Введите сомменарий')
    comment =  input()

    
    with file_path.open(mode='r', encoding='utf-8') as file:

        content = json.load(file)
        last_key = [_ for _ in content.keys()][-1]
        last_key = int(last_key.split('_')[1])
        last_key += 1
        last_key = str(f'row_{last_key}')
    
    with file_path.open(mode='w', encoding='utf-8') as file:
        
        nem_content = {'name': name, 'phone': phone, 'comment': comment}
        content[last_key] = nem_content

        json.dump(content, file, indent=4)
        
    return ('',menu_type,)

def fix_record(file_path):
    menu_type = 'top'
    print('fix_record')
    return ('',menu_type,)

def delete_record():
    menu_type = 'top'
    print('delete_record')
    return ('',menu_type,)

def show_record(file_path):
    
    import pandas as pd

    menu_type = 'top'
    
    print('Введите имя для поиска')
    name =  input()

    
    with file_path.open(mode='r', encoding='utf-8') as file:

        content = json.load(file)
        
    

    return ('',menu_type,)

def show_all_records():
    menu_type = 'top'
    print('show_all_records')
    return ('',menu_type,)

def exit_():
    print('''
              ---------------------------------------
              Вы вышли из программы!
              ---------------------------------------
              ''')
    exit()
