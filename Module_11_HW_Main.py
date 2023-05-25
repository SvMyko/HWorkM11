from collections import UserDict
from datetime import datetime, timedelta
import re
from Module_11_HW_Class import AddressBook
from Module_11_HW_Class import Record
from Module_11_HW_Class import Birthday
from Module_11_HW_Class import Name
from Module_11_HW_Class import Phone

def main():
    address_book = AddressBook()
    print("How can I help you?")
    while True:
        user_input = input().lower()
        if user_input == "hello":
            print("How can I help you?")
        # Додаємо новий контакт
        elif user_input.startswith("add contact"):
            try:
                user_input = input("Enter name and phone number separated by a space: ")
                name, *phones = user_input.split()
                if name in address_book.data:
                    print("Name already exist in the AddressBook")
                    continue
                else:
                    name = Name(name)
                    phones = [Phone(p) for p in phones]
                    record = Record(name, phones)
                    # Додаємо номер в книгу контактів
                    address_book.add_record(record)
                    print(f"Name: {name}, Phone: {record} added to Contact list")
            except ValueError:
                print("ERROR: Phone number should be in format +380XXXXXXXXX. Please enter a command again")
        # Змінюємо номер телефону
        elif user_input.startswith("change"):
            try:
                name = input("Enter name: ")
                record = address_book.get_phone(name)
                if not record:
                    print('Contact doesnt exist')
                    continue
                current_phone = input("Enter curent phone number: ")
                new_phone = input("Enter new phone number: ")
                # Змінюємо номер
                record.edit_phone(current_phone, new_phone)
                print(f"Name: {name}, Phone: {current_phone} changed to {new_phone}")
            except ValueError:
                print(f"Name: {AddressBook.name}, Phone: {AddressBook.phone}")
        # Видаляємо непотрібний номер
        elif user_input.startswith("delete"):
            try:
                name = input("Enter name: ")
                record = address_book.get_phone(name)
                if not record:
                    print('Contact doesnt exist')
                    continue
                current_phone = input("Enter curent phone number: ")
                # видаляємо номер
                record.del_phone(current_phone)
                print(f"Name: {name}, Phone: {current_phone} has been deleted")
            except ValueError:
                print(f"Name: {AddressBook.name}, Phone: {AddressBook.phone}")
        # Виводимо потрібний номер на екран
        elif user_input.startswith("phone"):
            try:
                name = input("Enter a contact name: ")
                record = address_book.get_phone(name)
                print(f"Name: {name}, Phone(s):  {record}")
            except IndexError:
                print("Please enter a name")
        # Виводимо  всі контакти на екран
        elif user_input == "show all":

            print(f'List of contacts: \n{address_book}')

        # Додаємо день народження
        elif user_input.startswith("add birthday"):
            try:
                name = input("Enter a contact name: ")

                record = address_book.get_phone(name)
                if not record:
                    print('Contact does not exist')
                    continue
                birthday_list = record.birthday
                if len(birthday_list) >= 1:
                    print('Date already exist')
                    continue
                else:
                    birthday_str = input("Enter a date of birthday in format DD.MM.YYYY: ")
                    birthday_class = Birthday(birthday_str)
                    birthday = datetime.strptime(birthday_class.value, "%d.%m.%Y")
                    record.add_birthday(birthday)
                    print(f"{name} birthday ({birthday.strftime('%d.%m.%Y')}) has been added")

            except ValueError:
                print("Incorrect date format. Date must be in the format DD.MM.YYYY. Please, enter the command again.")

        # Виводимо кількість днів до дня народження
        elif user_input.startswith("show birthday"):
            try:
                name = input("Enter a contact name: ")
                birthday_list = address_book.get_birthday(name)
                formatted_date = birthday_list.strftime('%d.%m.%Y')
                record = Record(name)
                counter = record.days_to_birthday(birthday_list)
                print(f"{name}'s birthday: {formatted_date}, in  {counter} day(s)")
            except IndexError: print("Please enter a name")

        #пагінація
        elif user_input.startswith("show"):
            address_book.iterator = iter(address_book)
            if address_book.iterator is None:
                print('Please use "show" command first to display the address book.')
            else:
                try:
                    page = next(address_book.iterator)
                except StopIteration:
                    print("End of address book.")
                    address_book.iterator = None
                else:
                    for name, record in page:
                        print(f"{name}: {record}")
        elif user_input.startswith("next"):
            if address_book.iterator is None:
                print('Please use "show" command first to display the address book.')
            else:
                try:
                    page = next(address_book.iterator)
                except StopIteration:
                    print("End of address book.")
                    address_book.iterator = None
                else:
                    for name, record in page:
                        print(f"{name}: {record}")

        elif user_input in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("I do not understand, please try again")

if __name__ == "__main__":
    main()
