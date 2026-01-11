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

def delete_telephone_book(dir):

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

        print('''
              ---------------------------------------
              Новый контакт сохранен!
              ---------------------------------------
              ''')
    
    show_all_records(file_path)
        
    return ('',menu_type,)

def show_record(file_path):
    
    import pandas as pd

    menu_type = 'top'

    with file_path.open(mode='r', encoding='utf-8') as file:

        content = json.load(file)

    
    df = pd.DataFrame.from_dict(content, orient='index')

    ### добавить поиск по другим полям.
    print('Выберите поле для поиска.')

    menu = {
        '1':('name'),
        '2':('phone')
    }  
    for key, item in menu.items():

        print(key, item)
    
    field =  input()

    if field == '1':

        print('Введите имя для поиска')
        name =  input()
        df = df[df['name'] == name]

    elif field == '2':
        
        print('Введите телефон для поиска')
        phone =  input()
        df = df[df['phone'] == phone]

    else:
        print('''
              ---------------------------------------
              Выбранное поле не существует. Попробуйте еще раз!
              ---------------------------------------
              ''')
        
        return ('',menu_type,)

    if not df.empty:
        print(df)
    else: 
        print('''
              ---------------------------------------
              Контакт не найден. Попробуйте еще раз!
              ---------------------------------------
              ''')

    return ('',menu_type,)

def show_all_records(file_path):
    menu_type = 'top'
    
    import pandas as pd

    menu_type = 'top'
    
    print('-------------Контакты------------')


    
    with file_path.open(mode='r', encoding='utf-8') as file:

        content = json.load(file)
    
    df = pd.DataFrame.from_dict(content, orient='index')
    
    print(df)

    print('---------------------------------')

    return ('',menu_type,)



    return ('',menu_type,)

def fix_record(file_path):
    
    import pandas as pd

    menu_type = 'top'

    with file_path.open(mode='r', encoding='utf-8') as file:

        content = json.load(file)

    
    df = pd.DataFrame.from_dict(content, orient='index')

    print('Выберите поле для поиска контакта на изменение.')

    menu = {
        '1':('name'),
        '2':('phone'),
        '3':('commet'),
        '4':('Изменить все.')

    }  
    for key, item in menu.items():

        print(key, item)
    
    field =  input()

    if field == '1':

        show_all_records(file_path)

        print('Введите имя контакта.')
        name =  input()

        index = df[df['name'] == name ].index[:]

        if not index.empty:

            content[index]['name'] = input('Новое имя: ')
            
        else:

            print('''
              ---------------------------------------
              Выбранное имя не существует. Попробуйте еще раз!
              ---------------------------------------
              ''')
        
            return ('',menu_type,)

    elif field == '2':
        
        show_all_records(file_path)

        print('Введите телефон')
        phone =  input()

        index = df[df['phone'] == phone ].index[:]

        if not index.empty:

            content[index]['phone'] = input('Новый телефон: ')
            
        else:

            print('''
              ---------------------------------------
              Выбранное имя не существует. Попробуйте еще раз!
              ---------------------------------------
              ''')
        
            return ('',menu_type,)
    
    elif field == '3':
        
        show_all_records(file_path)

        print('Введите телефон для изменения комментарий')
        phone =  input()

        index = df[df['phone'] == phone].index[:]

        if not index.empty:

            content[index]['comment'] = input('Новый comment: ')
            
        else:

            print('''
              ---------------------------------------
              Контакт с таким номером не существует. Попробуйте еще раз!
              ---------------------------------------
              ''')
        
            return ('',menu_type,)
        
    elif field == '4':
        
        show_all_records(file_path)

        print('Введите телефон')
        phone =  input()

        index = df[df['phone'] == phone].index[:]

        if not index.empty:

            content[index]['name'] = input('Новое имя: ')
            content[index]['phone'] = input('Новый телефон: ')
            content[index]['comment'] = input('Новый комментарий: ')
            
        else:

            print('''
              ---------------------------------------
              Контакт с таким номером не существует. Попробуйте еще раз!
              ---------------------------------------
              ''')
        
            return ('',menu_type,)

    else:
        print('''
              ---------------------------------------
              Выбранное поле не существует. Попробуйте еще раз!
              ---------------------------------------
              ''')
        
        return ('',menu_type,)

        
    with file_path.open(mode='w', encoding='utf-8') as file:

        json.dump(content, file, indent=4)
    
    print('''
            ---------------------------------------
            Контакт был изменен.
            ---------------------------------------
            ''')
    
    show_all_records(file_path)

    return ('',menu_type,)

def delete_record(file_path):
    menu_type = 'top'
    
    import pandas as pd

    menu_type = 'top'

    with file_path.open(mode='r', encoding='utf-8') as file:

        content = json.load(file)

    
    df = pd.DataFrame.from_dict(content, orient='index')

    ### добавить поиск по другим полям.
    print('Выберите поле для поиска контакта на удаление.')

    menu = {
        '1':('name'),
        '2':('phone')
    }  
    for key, item in menu.items():

        print(key, item)
    
    field =  input()

    if field == '1':

        print('Введите имя')
        name =  input()
        index = df[df['name'] == name ].index
        
        if not index.empty: 
            del content[index[0]]
        else:
            print('''
              ---------------------------------------
              Выбранный контакт существует. Попробуйте еще раз!
              ---------------------------------------
              ''')
        
            return ('',menu_type,)

    elif field == '2':
        
        print('Введите телефон')
        phone =  input()
        index = df[df['phone'] == phone].index

        if not index.empty: 
            del content[index[0]]
        else:
            print('''
              ---------------------------------------
              Выбранный контакт существует. Попробуйте еще раз!
              ---------------------------------------
              ''')
        
            return ('',menu_type,)

    else:
        print('''
              ---------------------------------------
              Выбранное поле не существует. Попробуйте еще раз!
              ---------------------------------------
              ''')
        
        return ('',menu_type,)

    if not index[0]:
        print('''
              ---------------------------------------
              Контакт не найден. Попробуйте еще раз!
              ---------------------------------------
              ''')
    else: 
        
        with file_path.open(mode='w', encoding='utf-8') as file:

            json.dump(content, file, indent=4)
        
        print('''
                ---------------------------------------
                Контакт был удален.
                ---------------------------------------
                ''')
        
        show_all_records(file_path)

    return ('',menu_type,)

def exit_():
    print('''
              ---------------------------------------
              Вы вышли из программы!
              ---------------------------------------
              ''')
    exit()
