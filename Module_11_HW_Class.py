from collections import UserDict
from datetime import datetime, timedelta
import re

# декоратор обробки помилок
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "This contact does not exist"
        except ValueError:
            return "Please enter name and phone number separated by a space"
        except IndexError:
            return "Please enter a contact name"
    return inner


class Field:
    value: str

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class Name(Field):
    pass


class Phone(Field):
    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str):
        if not value.startswith("+380") or not value[4:].isdigit() or len(value) != 13:
            raise ValueError
        self._value = value


class Birthday(Field):

    @property
    def value(self)-> str:
        return self._value

    @value.setter
    def value(self, value):
        date_pattern = r'^\d{2}\.\d{2}\.\d{4}$'
        if not re.match(date_pattern, value):
            raise ValueError
        self._value = value


@input_error
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

@input_error
class AddressBook(UserDict):
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

    # def __iter__(self):
    #     self.keys = list(self.data.keys())
    #     self.current_page = 0
    #     return self
    #
    # def __next__(self):
    #     if self.current_page >= len(self.keys):
    #         raise StopIteration
    #     page_keys = self.keys[self.current_page:self.current_page+10]
    #     page_records = [self.data[key] for key in page_keys]
    #     self.current_page += 3
    #     return page_records
