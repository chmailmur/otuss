import pytest 
import pandas as pd
from app.model.dictionary import PhoneBook

@pytest.fixture()
def phonebook(tmp_path):
    file = tmp_path / 'phone_book.csv'
    return PhoneBook(file)

@pytest.mark.parametrize("filename, exeption",
                         [
                            ('notfound.json',FileNotFoundError),
                            ('file.txt', FileNotFoundError)
                        ]
)
def test_read_pb_negative(phonebook, tmp_path, filename, exeption):
    pb = phonebook
    pb.phone_book_path = tmp_path/filename
    with pytest.raises(exeption):
        pb._read_pb()

def test_read_pb_positive(phonebook):
    pb = phonebook
    result = pb._read_pb()
    assert isinstance(result, pd.DataFrame)

@pytest.mark.parametrize("content, exeption",
                         [
                            ({}, TypeError),
                            ({ "15": {
                                        "na": "Рома",
                                        "phone": 124,
                                        "comment": ""}
                            }, TypeError),
                            (None, TypeError)
                        ]
)
def test_write_pb_negative(phonebook, content, exeption):
    pb = phonebook
    with pytest.raises(exeption):
        pb._write_pb(content)

@pytest.mark.parametrize('data_set', [
    {"name":'Рома', "phone":'124', "comment":'прогер'},
    {"name":'Рома', "phone":124, "comment":''}
])
def test_create_contact_positiv(phonebook, data_set):
    pb = phonebook
    assert pb.create_contact(data_set) is True

@pytest.mark.parametrize('data_set, exeption', [
    ({"name":'', "phone":'', "comment":''}, AttributeError), 
    ({"name", "phone"}, ValueError),
    (None, ValueError)
])
def test_create_contact_negativ(phonebook, data_set, exeption):
    pb = phonebook
    with pytest.raises(exeption):
        pb.create_contact(data_set)

@pytest.mark.parametrize('data_set, exeption',[
    ({"field":''}, ValueError), 
    ({"contact":''}, ValueError), 
    ({"field":'',"contact":''}, AttributeError), 
    ({''}, ValueError),
    (None, ValueError)
])
def test_search_contact_negative(phonebook, data_set, exeption):
    pb = phonebook
    with pytest.raises(exeption):
        pb.search_contact(data_set)

@pytest.mark.parametrize('contact',[
    48454,'sefs','54654','778'
])
def test_del_cocntact(phonebook, contact):
    pb = phonebook
    result = pb.del_cocntact(contact)
    assert isinstance(result, pd.DataFrame)

@pytest.mark.parametrize('dict, contact, new_dict, exeption', [
    ({"name":'Рома', "phone":'124', "comment":'прогер'},  {"contact":[124]},[], ValueError),
   ( {"name":'Рома', "phone":124, "comment":''},  {"contact":[124]},{"name":'', "phone":5654},AttributeError)
])
def test_change_contact_negativ(phonebook, dict, contact, new_dict, exeption):
    pb = phonebook
    pb.create_contact(dict)
    with pytest.raises(exeption):
        pb.change_contact(contact, new_dict)

@pytest.mark.parametrize('dict, contact, new_dict', [
    ({"name":'Рома', "phone":'124', "comment":'прогер'},  {"contact":[124]}, {"name":'Илья', "phone":7787, "comment":'прогер'}),
   ({"name":'Кира', "phone":124, "comment":''},   {"contact":[124]} , {"name":'Мумия'})
])
def test_change_contact_positive(phonebook, dict, contact, new_dict):
    pb = phonebook
    pb.create_contact(dict)
    result = pb.change_contact(contact, new_dict)
    assert isinstance(result, pd.DataFrame)

