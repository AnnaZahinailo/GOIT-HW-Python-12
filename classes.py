from collections import UserDict
from datetime import date, datetime
import pickle
import re


class Field:
    def __init__(self, value):
        if not isinstance(value, str):
            raise ValueError("Value must be a string")
        self.value = value
    
    def __str__(self) -> str:
        return str(self.value)


class Name(Field): 
    pass


class Phone(Field):
    @property
    def value (self):
        return self.__value

    @value.setter
    def value(self, value):
        if value and not re.match(r"^\+[\d]{12}$", value):
            raise ValueError
        self.__value = value


class Birthday(Field):
    def __init__(self, value=None):
        self.value = value
    
    @property
    def value (self):
        return self.__value

    @value.setter
    def value(self, value):
        if value is not None and not re.match(r"^\d{2}\.\d{2}\.\d{4}$", value):
            raise ValueError("Birthday should be in format dd.mm.yyyy") #from ValueError
        try:
            datetime.strptime(value, '%d.%m.%Y'), datetime
        except ValueError:
            return "Date value is not correct"
        self.__value = value


class Record:
    def __init__(self, name:Name) -> None:
        self.name = name
        self.phone = None
        self.birthday = None

    phone_list = []

    def add_phone(self, phone:Phone):
        if phone:
            self.phone_list.append(phone.value)

    def change_phone(self, phone:Phone, new_phone:Phone):
        ind = self.phone_list.index(phone.value)
        self.phone_list[ind] = new_phone.value

    def delete_phone(self, phone:Phone):
        if phone.value in self.phone_list:
            self.phone_list.remove(phone.value)

    def add_birthday(self, birthday:Birthday):
        if birthday:
            self.birthday = birthday

    def days_to_birthday(self, birthday:Birthday):
        if birthday:
            today = date.today()
            self.birthday = birthday
            date_of_birth = datetime.strptime(self.birthday, '%d.%m.%Y')
            try:
                bd = date(today.year, date_of_birth.month, date_of_birth.day)
            except ValueError:
                bd = date(today.year, date_of_birth.month, date_of_birth.day-1)
            if bd < today:
                bd = bd.replace(year=today.year + 1)
        return abs((bd - today).days)


class AddressBook(UserDict):

    def add_record(self, record:Record):
        self.data[record.name.value] = record.phone_list, (record.birthday.value if record.birthday else None)

    def iterator(self, n):
        i = 0
        j = 0
        l = len(self.data)
        page_dict = {}
        for par in self.data:
            if j < n:
                j += 1
                i += 1
                page_dict.update({par: self.data.get(par)})       
            if j == n or i == l:
                yield page_dict
                page_dict = {}
                j = 0

    def upload_dict(self, file_name):
        with open(file_name, "rb") as fh:
            upload = pickle.load(fh)
            self.data.clear()
            self.data.update(upload)

    def save_dict(self, file_name):
        with open(file_name, "wb") as fh:
            pickle.dump(self.data, fh)        

    def find_txt(self, txt, case_mode):
        result = {}
        for name in self.data:
            phones = self.data[name][0]
            if case_mode == "s" and name.find(txt) != -1:
                result.update({name: self.data.get(name)})            
            elif case_mode != "s" and name.lower().find(txt.lower()) != -1:
                result.update({name: self.data.get(name)})
            else:
                for phone in phones:
                    if phone.find(txt) != -1:
                        result.update({name: self.data.get(name)})
        return result
