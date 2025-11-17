import re
from datetime import datetime

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found"
        except ValueError:
            return "Give me name and phone please"
        except IndexError:
            return "Enter user name"
    return wrapper

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not re.match(r"^\d{10}$", value):
            raise ValueError("Phone must be exactly 10 digits")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

@input_error
def add_birthday( args, book):
    name = args[0]
    date_str = args[1]
    
    if name not in book.data:
        print("Contact not found.")
        return
    
    birthday = Birthday(date_str)
    book.data[name].birthday = birthday
    print(f"Birthday added for {name}: {birthday}")

@input_error
def show_birthday(args, book):
    name = args[0]
    if name not in book.data:
        print("Contact not found.")
        return
    
    record = book.data[name]
    if "birthday" in record.__dict__:
        print(f"{name}'s birthday is {record.birthday}")
    else:
        print(f"No birthday set for {name}")


@input_error
def birthdays(args, book):
    for record in book.list_all():
        if "birthday" in record.__dict__:  # safe check without hasattr
            print(f"{record.name.value}: {record.birthday}")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, number):
        self.phones.append(Phone(number))

    def remove_phone(self, number):
        for phone in self.phones:
            if phone.value == number:
                self.phones.remove(phone)
                return True
        return False

    def change_phone(self, old, new):
        if self.remove_phone(old):
            self.add_phone(new)
            return True
        return False

    def find_phone(self, number):
        for phone in self.phones:
            if phone.value == number:
                return True
        return False

    def __str__(self):
        phones_str = "; ".join(str(p) for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"


class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        return False

    def find(self, name):
        result = []
        for key, record in self.data.items():
            if name.lower() in key.lower():
                result.append(record)
        return result

    def list_all(self):
        return list(self.data.values())


def main():
    book = AddressBook()

    while True:
        command = input("\nEnter command (add, delete, edit, find, list, exit): ").strip().lower()

        if command == "add":
            name = input("Enter name: ")
            phone = input("Enter phone (10 digits): ")
            try:
                record = book.data.get(name, Record(name))
                record.add_phone(phone)
                book.data[name] = record
                print("Contact added")
            except ValueError as e:
                print(f"Error: {e}")

        elif command == "delete":
            name = input("Enter name to delete: ")
            if book.delete(name):
                print("Contact deleted.")
            else:
                print("Contact not found.")
        elif command == "hello":
            print("how can I help you")

        elif command == "change":
            name = input("Enter name to change: ")
            if name in book.data:
                old_phone = input("Enter old phone number: ")
                new_phone = input("Enter new phone number: ")
                if book.data[name].change_phone(old_phone, new_phone):
                    print("Phone changed.")
                else:
                    print("Old phone number not found.")
            else:
                print("Contact not found.")

        elif command == "phone":
            name = input("enter name to search: ")
            if name in book.data:
                print(book.data[name])
            else:
                print("no contacts found.")

        elif command == "all":
            for r in book.list_all():
                print(r)

        elif command == "add-birthday":
            args = input("Enter name and birthday (DD.MM.YYYY) separated by space: ").split()
            add_birthday(args, book)

        elif command == "show-birthday":
            args = input("Enter name to show birthday: ").split()
            show_birthday(args, book)

        elif command == "birthdays":
            args = [] 
            birthdays(args, book)

        elif command == "exit":
            print("Bye")
            break

        else:
            print("Unknown command.")


if __name__ == "__main__":
    main()
