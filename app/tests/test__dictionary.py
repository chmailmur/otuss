import pytest 
from app.model.dictionary import PhoneBook

pb = PhoneBook()

def test_read_pb():
    pass

def test_write_pb():
    pass

@pytest.mark.parametrize('data_set', [
    {"name":'', "phone":'', "comment":''},
    {"name":'Рома', "phone":'124', "comment":'прогер'},
    {"name":'Рома', "phone":'124', "comment":''},
    {"name":'Рома', "phone":124, "comment":''},
    {"name", "phone"},
    None,

])
def test_create_contact(data_set):
    assert pb.create_contact(data_set) is True


def test_search_contact():
    pass

def test_del_cocntact():
    pass

def test_change_contact():
    pass



# Добавление контакта
# Поиск контакта (по имени, телефону и общему поисковому запросу)
# Изменение контакта
# Удаление контакта
