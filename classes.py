from collections import UserDict
import csv
from datetime import datetime, date
import re


class WrongPhone(Exception):
    pass


class WrongDate(Exception):
    pass


class WrongEmail(Exception):
    pass


class Field:
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if self.__class__ == other.__class__:
            return self._value == other.value
        return False

    # Додав магічний метод __hash__ тому, що діти класу Field
    # можуть бути елементами множини(set)
    def __hash__(self):
        return hash(self._value)


class Name(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val


class Phone(Field):

    @staticmethod
    def is_valid_phone(phone):
        # Валідація номеру телефону відбувається за
        # допомогою регулярнго виразу, що означає: необов'язково +, потім цифра від 1 до 9
        # та 11 цифр від 0 до 9. Тобто валідними будуть такі номери +123456987456 та 123456987456,
        match = re.search(r"^\+?[1-9][\d]{11}$", phone)
        return bool(match)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if self.is_valid_phone(val):
            self._value = val
        else:
            raise WrongPhone("You tried to enter an invalid phone number. "
                             "Please check the value and try again")


class Birthday(Field):

    @staticmethod
    def is_valid_date(date):
        # Валідація дня народження є значно простішою, ніж номеру телефону.
        # Якщо ввід користувача перетворюється у об'єкт datetime то дата валідна
        try:
            datetime.strptime(str(date), "%d.%m.%Y")
            return True
        except ValueError:
            return False

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if self.is_valid_date(val):
            self._value = val
        else:
            raise WrongDate(
                "Invalid date. Please enter birthday in format 'DD.MM.YYYY'.")


class Record:
    def __init__(self, name, phones=None, birthday=None, address=None, email=None):
        self.name = name
        self.phones = phones
        self.birthday = birthday
        self.address = address
        self.email = email

    def __str__(self):
        # Рядкове представлення Record у форматі
        # Володя: +123456987456, 23456987456. Birthday: 21.01.1978
        phones_str = ", ".join([str(phone) for phone in self.phones])
        birthday_str = f"Birthday: {self.birthday}" if self.birthday.value else ""
        address_str = f"Address: {self.address}" if self.address else ""
        email_str = f"Email: {self.email}" if self.email else ""
        return f"{self.name.value}: {phones_str}. {birthday_str}. {address_str}.{email_str}"

    def __repr__(self):
        return str(self)

    def add_phone(self, phone: Phone):
        self.phones.append(phone)
        # Список телефонів приводиться до множини для того, щоб виключити можливість
        # повторення номеру телефону
        self.phones = list(set(self.phones))
        return f"Phone number {phone} for user {self.name.value} added successfully."

    def change_phone(self, old_number: Phone, new_number: Phone):
        # У списку телефонів знаходиться індекс старого номера та змінює
        # old_number на new_number
        if old_number not in self.phones:
            return f"Number {old_number} not found."
        else:
            phone_number_index = self.phones.index(old_number)
            self.phones[phone_number_index] = new_number
            return f"The phone number {old_number} for the user {self.name} "\
                f"has been changed to {new_number}"

    def delete_phone(self, phone):
        try:
            self.phones.remove(phone)
            return f"Phone number {phone} for user {self.name} deleted successfully."
        except ValueError:
            return f"Phone number {phone} for user {self.name} not found"

    def days_to_birthday(self):
        try:
            birthday = datetime.strptime(str(self.birthday), "%d.%m.%Y").date()
        except ValueError:
            return f"No birthday for user {self.name.value}"

        today = date.today()
        birthday = birthday.replace(year=today.year)

        if birthday < today:
            birthday = birthday.replace(year=today.year+1)
        result = (birthday - today).days
        birthday_str = birthday.strftime("%d %B")
        return f"The birthday of user {self.name} will be in {result} days, {birthday_str}"


class Address:
    def __init__(self, street="", city="", country="", postcode=""):
        self.street = street
        self.city = city
        self.country = country
        self.postcode = postcode

    def __str__(self):
        return f"{self.street},{self.city},{self.country},{self.postcode}"

    def __repr__(self):
        return f"Address(street='{self.street}', city='{self.city}', country='{self.country}', postcode='{self.postcode}')"


class Email:
    def __init__(self, value=""):
        self.value = value

    @staticmethod
    def is_valid_email(email):
        match = re.search(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)
        return bool(match)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if self.is_valid_email(val):
            self._value = val

        else:
            raise WrongEmail(
                "Invalid email address. Please enter a correct email address")

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return str(self)


class AddressBook(UserDict):
    def add_record(self, record):
        self[record.name.value] = record

    def delete_record(self, name: Name):
        del self[name.value]

    def change_record(self, name, new_record):
        self[new_record.name.value] = new_record

    def search(self, field: str, text: str) -> list[Record]:
        result = []
        if field.lower() == "name":
            for record in self.data.values():
                if text in record.name.value:
                    result.append(record)
        elif field.lower() == "phone":
            for record in self.data.values():
                for phone in record.phones:
                    if text in phone.value:
                        result.append(record)
                        break

        elif field.lower() == "address":
            for record in self.data.values():
                if text.lower() in str(record.address).lower():
                    result.append(record)

        elif field.lower() == "email":
            for record in self.data.values():
                if record.email and text.lower() in record.email.value.lower():
                    result.append(record)

        return result

    @classmethod
    def open_file(cls, filename):
        """Take as input filename. Return AddressBook"""
        try:
            with open(filename, encoding="utf-8") as file:
                reader = csv.DictReader(file)
                data = cls()
                for row in reader:
                    username = Name(row["Name"])
                    # Формат csv не пітримує масивів. Тому для запису номерів телефону
                    # довелося користатися таким не дуже красивим способом: записувати
                    # телефони у як рядки
                    phones_str = re.sub(r"\[|\]|\ ", "",
                                        row["Phone numbers"]).split(",")
                    phones = [Phone(phone) for phone in phones_str]
                    birthday = Birthday(row["Birthday"])
                    address = Address(
                        row["Street"], row["City"], row["Country"], row["Postcode"])
                    email = Email(row["Email"]) if row["Email"] else None

                    # Тут з усіх даних створюється Record та записується до data,
                    # що є екземпляром AddressBook
                    record = Record(username, phones, birthday, address, email)
                    data[record.name.value] = record
        except FileNotFoundError:
            data = cls()
        return data

    def write_to_csv(self, filename: str):
        fieldnames = ["Name", "Phone numbers", "Birthday",
                      "Street", "City", "Country", "Postcode", "Email"]

        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for record in self.data.values():
                writer.writerow(
                    {"Name": record.name,
                     "Phone numbers": record.phones,
                     "Birthday": record.birthday,
                     "Street": record.address.street,
                     "City": record.address.city,
                     "Country": record.address.country,
                     "Postcode": record.address.postcode,
                     "Email": record.email.value if record.email else ""})

    # Методи __iter__ та __next__ перетворюють елземпляри AddressBook на
    # ітератори, щоб користувачам показувати одночасно self.page_size записів

    def __iter__(self):
        self.current_page = 1
        self.page_size = 10
        self.start_index = (self.current_page - 1) * self.page_size
        self.end_index = self.start_index + self.page_size
        return self

    def __next__(self):
        if self.start_index >= len(self.data):
            raise StopIteration

        page_records = list(self.data.values())[
            self.start_index:self.end_index]
        self.start_index = self.end_index
        self.end_index = self.start_index + self.page_size
        self.current_page += 1

        return page_records
