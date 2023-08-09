import os
import platform
import sys

import classes
from notes import NoteBook
from clean import main


commands = {}

# Декоратор set_commands створений для наповнення словника commands
# Ключами є команда, котра передається у якості аргумента name та, за потреби,
# additional. Значеннями є функції, що виконуються при введенні команди


def set_commands(name, *additional):
    def inner(func):
        commands[name] = func
        for command in additional:
            commands[command] = func
    return inner


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except (IndexError, ValueError):
            return "Enter all require arguments please.\nTo see more info type 'help'."
        except classes.WrongPhone:
            return "You tried to enter an invalid phone number. Please check the value and try again"
        except classes.WrongDate:
            return "Invalid date. Please enter birthday in format 'DD.MM.YYYY'."
        except classes.WrongEmail:
            return "Invalid email address. Please enter a correct email address."
        except KeyError:
            return "Id not found. Please check the value and try again"
    # Рядок нижче потрібний для того, щоб пов'язати функції та їх рядки документації.
    # Це потрібно для функції help.
    inner.__doc__ = func.__doc__
    return inner



@set_commands("add")
@input_error
def add(*args):
    """Take as input username, phone number, birthday, address, email and add them to the base.
    If username already exist add phone number to this user."""
    name = classes.Name(args[0])
    # Два блоки if, розміщених нижче відповідають за правильність введення телефону
    # та дня народження. Якщо значення невалідне, викликається помилка, що потім обробляється
    # деораторот input_error
    if classes.Phone.is_valid_phone(args[1]):
        phone_number = [classes.Phone(args[1])]
    else:
        raise classes.WrongPhone
    birthday = None
    if len(args) > 2:
        if classes.Birthday.is_valid_date(args[2]):
            birthday = classes.Birthday(args[2])
        else:
            raise classes.WrongDate
    address = classes.Address(street=args[3], city=args[4],
                              country=args[5], postcode=args[6])

    email_value = args[7]
    if not classes.Email.is_valid_email(email_value):
        raise classes.WrongEmail

    email = classes.Email(email_value)
    # У змінній data зберігається екземпляр класу AddressBook із записаними раніше контактами
    # Змінна name_exists показує, чи існує контакт з таким ім'ям у data
    data = classes.AddressBook.open_file("data.json")
    name_exists = bool(data.get(name.value))

    # Тут відбувається перевірка, чи ім'я вже є у списку контактів
    # Якщо контакт відсутній, створюється новий Record.
    # Якщо присутній - до існуючого екземпляру Record додається номер телефону
    if name_exists and phone_number:
        # Методи класу Record повертають повідомлення для користувача
        # Дані повідомлення записуються у змінну та повертаються з функції
        # для показу користувачу
        msg = data[name.value].add_phone(phone_number)
    elif not phone_number:
        raise IndexError
    else:
        record = classes.Record(name, phone_number, birthday, address, email)
        data.add_record(record)
        msg = f"User {name} added successfully."

    data.write_to_file("data.json")
    return msg


@set_commands("birthday")
@input_error
def days_to_birthday_handler(*args):
    """Take as input username and show the number of days until his birthday"""
    name = classes.Name(args[0])
    data = classes.AddressBook.open_file("data.json")
    name_exists = bool(data.get(name.value))

    if not name_exists:
        return f"User {name} not found"

    return data[name.value].days_to_birthday()


@set_commands("showbd")
@input_error
def show_birthdays_handler(*args):
    """Take as input number of days and show the list of birthdays.
    The MAX number of days is 365"""
    try:
        value = int(args[0])
    except:
        return "Please enter the valid command: showbd number_of_days"
    if type(value) == int and value > 0:
        data = classes.AddressBook.open_file("data.json")
        if value > 365:
            value = 365
        return data.show_birthday(value)
    else:
        return "Please input a valid number of days"


@set_commands("change")
@input_error
def change(*args):
    """Take as input username, old and new phone number 
    and changes the corresponding data."""

    name = classes.Name(args[0])
    old_phone = classes.Phone(args[1])
    if classes.Phone.is_valid_phone(args[2]):
        new_phone = classes.Phone(args[2])
    else:
        raise classes.WrongPhone

    data = classes.AddressBook.open_file("data.json")
    name_exists = bool(data.get(name.value))

    if not name_exists:
        msg = f"Name {name} doesn`t exist. "\
            "If you want to add it, please type 'add user <name> <phone number>'."
    else:
        msg = data[name.value].change_phone(old_phone, new_phone)

    data.write_to_file("data.json")
    return msg


@set_commands("clear")
@input_error
def clear(*args):
    """Clear the console."""
    # Дана функція відповідальна за очищення консолі.
    # Darwin це macOS
    system = platform.system()
    if system == "Windows":
        os.system("cls")
    elif system in ("Linux", "Darwin"):
        os.system("clear")
    else:
        return "Sorry, this command is not available on your operating system."


@set_commands("del user")
@input_error
def delete_user(*args):
    """Take as input username and delete that user"""
    name = classes.Name(args[0])

    data = classes.AddressBook.open_file("data.json")
    name_exists = bool(data.get(name.value))

    if not name_exists:
        return f"Name {name} doesn`t exist."
    else:
        data.delete_record(name)

    data.write_to_file("data.json")
    return f"User {name} deleted successfully."


@set_commands("del phone")
@input_error
def delete_phone(*args):
    """Takes as input username and phone number and deletes that phone"""
    name = classes.Name(args[0])
    phone = classes.Phone(args[1])

    data = classes.AddressBook.open_file("data.json")
    name_exists = bool(data.get(name.value))

    if not name_exists:
        msg = f"Name {name} doesn`t exist."
    else:
        msg = data[name.value].delete_phone(phone)

    data.write_to_file("data.json")
    return msg


@set_commands("hello")
@input_error
def hello(*args):
    """Greet user."""
    return "How can I help you?"


@set_commands("help")
@input_error
def help_command(*args):
    """Show all commands available."""
    # Даний метод виводить користувачу перелік усіх команд з описом.
    # Створюється рядок all_commands, що наповнюється у циклі.
    # command це ключі в словнику commands.
    # func - значення. func.__doc__ це рядок документації, що додатково
    # прив'язувався до функції у декораторі input_error
    all_commands = ""
    for command, func in commands.items():
        all_commands += f"{command}: {func.__doc__}\n"
    return all_commands


@set_commands("phone")
@input_error
def phone(*args):
    """Take as input username and show user`s phone number."""
    name = classes.Name(args[0])

    data = classes.AddressBook.open_file("data.json")
    name_exists = bool(data.get(name.value))

    if not name_exists:
        return f"Name {name} doesn`t exist. "\
            "If you want to add it, please type 'add <name> <phone number>'."
    else:
        # У цьому рядку список телефонів перетворюється у рядок,
        # де номері перелічені через кому
        phone_numbers = ", ".join(str(phone)
                                  for phone in data[name.value].phones)
        if phone_numbers:
            return f"Phone numbers for {name}: {phone_numbers}."
        else:
            return f"There are no phone numbers for user {name}"


@set_commands("show all")
@input_error
def show_all(*args):
    """Show all users or notes"""
    field = args[0].lower()
    # Код функції show_all має саме такий вигляд тому, що AddressBook
    # це ітератор
    if field not in ("users", "notes"):
        return f"Unknown field {field}. Please type 'users' or 'notes'"
    if field == "users":
        return classes.AddressBook.open_file("data.json")
    return NoteBook.read_from_file()


@set_commands("search")
@input_error
def search_handler(*args):
    """Take as input searched field(name, phone, tag or text)
    and the text to be found. Returns all found users"""
    # у даній функції користувачу потрібно обрати, у яких полях
    # відбуватиметься пошук(наразі це name або phone) та ввести значення для пошуку.
    #  Функція повертає рядок з переліком усіх контаків
    field = args[0]
    text = " ".join(args[1:])
    if field.lower() not in ("name", "phone", "email","tag","text"):
        return f"Unknown field '{field}'.\nTo see more info enter 'help'"

    nb = NoteBook.read_from_file()
    if field == "text":
        return nb.find_notes_by_text(text)
    elif field == "tag":
        return nb.find_notes_by_keyword(text)

    ab = classes.AddressBook.open_file("data.json")
    result = ab.search(field, text)
    if not result:
        return "There are no users matching"
    return "\n".join([str(rec) for rec in result])


@set_commands("address")
@input_error
def address(*args):
    """Take the input username and show the address"""
    name = classes.Name(args[0])

    data = classes.AddressBook.open_file("data.json")
    name_exists = bool(data.get(name.value))

    if not name_exists:
        return f"Name {name} doesn't exist"

    else:
        address_str = str(data[name.value].address)
        if address_str:
            return f"Address for {name}: {address_str}."

        else:
            return f"There is no address for user {name}."


@set_commands("email")
@input_error
def email(*args):
    """Take the input username and show the email"""
    name = classes.Name(args[0])
    data = classes.AddressBook.open_file("data.json")
    name_exists = bool(data.get(name.value))

    if not name_exists:
        return f"Name {name} doesn't exist."

    else:
        email_str = str(data[name.value].email)

        if email_str:
            return f"Email for {name}: {email_str}."

        else:
            return f"There isn't email for user {name}."


@set_commands("create_note")
@input_error
def create_note(*args):
    """Take as input the text of the note in quotes and adds it to the notebook"""
    text = " ".join(args)
    nb = NoteBook.read_from_file()
    nb.add_note(text)

    nb.save_to_file()
    return "Note added successfully."


@set_commands("edit_note")
@input_error
def edit_note(*args):
    """Take as input note id and change selected note"""
    note_id = args[0]
    nb = NoteBook.read_from_file()
    nb.edit_note(note_id)

    nb.save_to_file()
    return "Note edited successfully."


@set_commands("del note")
@input_error
def del_note(*args):
    """Take the input username and show the address"""
    name = classes.Name(args[0])
    data = classes.AddressBook.open_file("data.csv")
    name_exists = bool(data.get(name.value))

    if not name_exists:
        return f"Name {name} doesn't exist."

    else:
        email_str = str(data[name.value].email)

        if email_str:
            return f"Email for {name}: {email_str}."

        else:
            return f"There isn't email for user {name}."


@set_commands("sort notes")
@input_error
def sort_notes(*args):
    """Takes a keyword as input and sorts notes by it"""
    keyword = args[0]
    nb = NoteBook.read_from_file()
    return nb.sort_notes(keyword)

@set_commands("sort files")
@input_error
def sort_files(*args):
    """Sort files by categories in input directory"""
    return main()


@set_commands("add_phone")
@input_error
def add_phone(*args):
    """Takes as input username, phone number and adds to the contact."""

    name = classes.Name(args[0])
    if classes.Phone.is_valid_phone(args[1]):
        new_phone = classes.Phone(args[1])
    else:
        raise classes.WrongPhone

    data = classes.AddressBook.open_file("data.json")
    name_exists = bool(data.get(name.value))
    if not name_exists:
        msg = f"Name {name} doesn't exist. "\
            "If you want to add it, please use add command."
    else:
        msg = data[name.value].add_phone(new_phone)

    data.write_to_file("data.json")
    return msg


@set_commands("change_birthday")
@input_error
def change_birthday(*args):
    """Takes as input username, birthday date
    and changes the corresponding data."""

    name = classes.Name(args[0])
    if classes.Birthday.is_valid_date(args[1]):
        new_birthday = classes.Birthday(args[1])
    else:
        raise classes.WrongDate(
                "Invalid date. Please enter birthday in format 'DD.MM.YYYY'.")

    data = classes.AddressBook.open_file("data.json")
    name_exists = bool(data.get(name.value))
    if not name_exists:
        msg = f"Name {name} doesn`t exist. "\
            "If you want to add it, please type 'add user <name> <phone number>'."
    else:
        msg = data[name.value].change_birthday(new_birthday)

    data.write_to_file("data.json")
    return msg


@set_commands("change_address")
@input_error
def change_address(*args):
    """Takes as input username, new address and changes the corresponding data."""

    if len(args) < 5:
        return "Not valid command format."\
            "Please enter correct address data"
    name = classes.Name(args[0])
    data = classes.AddressBook.open_file("data.json")
    name_exists = bool(data.get(name.value))
    if not name_exists:
        msg = f"Name {name} doesn't exist. "\
            "If you want to add it, please use add command."
    else:
        address = classes.Address(street=args[1], city=args[2],
                              country=args[3], postcode=args[4])
        msg = data[name.value].change_address(address)

    data.write_to_file("data.json")
    return msg


@set_commands("change_email")
@input_error
def change_email(*args):
    """Takes as input username, new email and changes the corresponding data."""

    name = classes.Name(args[0])
    data = classes.AddressBook.open_file("data.json")
    name_exists = bool(data.get(name.value))
    if not name_exists:
        msg = f"Name {name} doesn't exist. "\
            "If you want to add it, please use add command."
    else:
        email_value = args[1]
        if not classes.Email.is_valid_email(email_value):
            raise classes.WrongEmail
        new_email = classes.Email(email_value)
        msg = data[name.value].change_email(new_email)

    data.write_to_file("data.json")
    return msg


@set_commands("exit", "close", "good bye")
@input_error
def exit(*args):
    """Interrupt program."""
    sys.exit(0)

# Для того, щоб дадати нові команди до бота достатньо просто
# тут написати іх код з відповідними декораторами та docstring.
# Наприклад, уявімо, що потрібно додати команду, що повертатиме ввід користувача.
# Якщо розчоментувати кож нижче можна побачити, що команда echo працює успішно

# @set_commands("echo")
# @input_error
# def echo(*args):
#     """Return user`s input"""
#     return " ".join(args)
