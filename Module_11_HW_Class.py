from collections import UserDict
from datetime import datetime, timedelta
import re


class Field:

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

class Name(Field):

    pass


class Phone(Field):

    @Field.value.setter
    def value(self, value: str):
        if not value.startswith("+380") or not value[4:].isdigit() or len(value) != 13:
            raise ValueError
        Field.value.fset(self, value)


class Birthday(Field):

    @Field.value.setter
    def value(self, value):
        date_pattern = r'^\d{2}\.\d{2}\.\d{4}$'
        if not re.match(date_pattern, value):
            raise ValueError
        Field.value.fset(self, value)



class Record:
    def __init__(self, name, phones=None, birthday=None):
        self.name = name
        self.birthday = birthday or list()
        self.phones = phones or list()

    def __str__(self):
        return ", ".join(p.value for p in self.phones)

    def add_birthday(self, birthday):
        self.birthday.append(birthday)

    def days_to_birthday(self, birthday):
        today = datetime.now().date()
        next_birthday = datetime(today.year, birthday.month, birthday.day).date()

        if next_birthday < today:
            next_birthday = datetime(today.year + 1, birthday.month, birthday.day).date()
        days_left = (next_birthday - today).days
        return days_left

    def add_phone(self, phone):
        self.phones.append(phone)

    def del_phone(self, current_phone):
        self.phones = [phone for phone in self.phones if phone.value != current_phone]

    def edit_phone(self, current_phone, new_phone):
        for phone in self.phones:
            if phone.value == current_phone:
                phone.value = new_phone
                return
        raise ValueError


class AddressBook(UserDict):
    iterator = None


    def add_record(self, record):
        self.data[record.name.value] = record

    def get_phone(self, name):
        return self.data.get(name)

    def get_birthday(self, name):
        record = self.data[name]
        birthday = record.birthday
        birthday_datetime = birthday[0]
        return birthday_datetime

    def get_all(self):
        return self.data.values()

    def __str__(self):
        return  "\n".join(f"{name}: {record}" for name, record in self.data.items())

    def __iter__(self):
        data = sorted(self.data.items())
        for index in range(0, len(data), 3):
            yield data[index:index + 3]

