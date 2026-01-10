from pathlib import Path
import json


def cheak_telephone_book(dir, path_file):

    if dir.is_dir() and path_file.exists():
        return True
    else:
        return False
    
    
    
def cheak_structure(path_file):

    with path_file.open(mode='r', encoding='utf-8') as file:

        data_list = file.read()

        data_list = json.loads(data_list)

    return False, [data_list[i].keys() for i in data_list.keys()]


def create_telephone_book(target_dir, target_file_path ):

    menu_type = 'top'
    
    stucture = {
        'row_0':{
            'name': '',
            'phone': '',
            'comment': '',
        }
    }     

    
    
    target_dir.mkdir(exist_ok=True)

    with target_file_path.open(mode='w', encoding='utf-8') as file:
        
        file.write(json.dumps(stucture, indent=4))

    print("Справочник был создан! Можно начать работу")
    
    return (True,menu_type,)



def create_record():
    menu_type = 'top'
    print('create_record')
    return ('',menu_type,)

def fix_record():
    menu_type = 'top'
    print('fix_record')
    return ('',menu_type,)

def delete_record():
    menu_type = 'top'
    print('delete_record')
    return ('',menu_type,)

def show_record():
    menu_type = 'top'
    print('show_record')
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
