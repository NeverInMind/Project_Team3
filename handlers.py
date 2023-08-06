import os
import platform
import sys

import classes

commands = {}


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

    inner.__doc__ = func.__doc__
    return inner


@set_commands("add")
@input_error
def add(*args):
    """Take as input username, phone number, birthday, address, email and add them to the base.
    If username already exist add phone number to this user."""
    name = classes.Name(args[0])
    if classes.Phone.is_valid_phone(args[1]):
        phone_number = classes.Phone(args[1])
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

    data = classes.AddressBook.open_file("data.csv")
    name_exists = bool(data.get(name.value))

    if name_exists and phone_number:
        msg = data[name.value].add_phone(phone_number)
    elif not phone_number:
        raise IndexError
    else:
        record = classes.Record(name, phone_number, birthday, address, email)
        data.add_record(record)
        msg = f"User {name} added successfully."

    data.write_to_csv("data.csv")
    return msg


@set_commands("birthday")
@input_error
def days_to_birthday_handler(*args):
    """Take as input username and show the number of days until his birthday"""
    name = classes.Name(args[0])
    data = classes.AddressBook.open_file("data.csv")
    name_exists = bool(data.get(name.value))

    if not name_exists:
        return f"User {name} not found"

    return data[name.value].days_to_birthday()


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

    data = classes.AddressBook.open_file("data.csv")
    name_exists = bool(data.get(name.value))

    if not name_exists:
        msg = f"Name {name} doesn`t exists. "\
            "If you want to add it, please type 'add user <name> <phone number>'."
    else:
        msg = data[name.value].change_phone(old_phone, new_phone)

    data.write_to_csv("data.csv")
    return msg


@set_commands("clear")
@input_error
def clear(*args):
    """Clear the console."""
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

    data = classes.AddressBook.open_file("data.csv")
    name_exists = bool(data.get(name.value))

    if not name_exists:
        return f"Name {name} doesn`t exists."
    else:
        data.delete_record(name)

    data.write_to_csv("data.csv")
    return f"User {name} deleted successfully."


@set_commands("del phone")
@input_error
def delete_phone(*args):
    """Take as input username and phone number and delete that phone"""
    name = classes.Name(args[0])
    phone = classes.Phone(args[1])

    data = classes.AddressBook.open_file("data.csv")
    name_exists = bool(data.get(name.value))

    if not name_exists:
        msg = f"Name {name} doesn`t exists."
    else:
        msg = data[name.value].delete_phone(phone)

    data.write_to_csv("data.csv")
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
    all_commands = ""
    for command, func in commands.items():
        all_commands += f"{command}: {func.__doc__}\n"
    return all_commands


@set_commands("phone")
@input_error
def phone(*args):
    """Take as input username and show user`s phone number."""
    name = classes.Name(args[0])

    data = classes.AddressBook.open_file("data.csv")
    name_exists = bool(data.get(name.value))

    if not name_exists:
        return f"Name {name} doesn`t exists. "\
            "If you want to add it, please type 'add <name> <phone number>'."
    else:

        phone_numbers = ", ".join(str(phone)
                                  for phone in data[name.value].phones)
        if phone_numbers:
            return f"Phone numbers for {name}: {phone_numbers}."
        else:
            return f"There are no phone numbers for user {name}"


@set_commands("show all")
@input_error
def show_all(*args):
    """Show all users."""
    return classes.AddressBook.open_file("data.csv")


@set_commands("search")
@input_error
def search_handler(*args):
    """Take as input searched field(name or phone)
    and the text to be found. Returns all found users"""
    # у даній функції користувачу потрібно обрати, у яких полях
    # відбуватиметься пошук(наразі це name або phone) та ввести значення для пошуку.
    #  Функція повертає рядок з переліком усіх контаків
    field = args[0]
    text = args[1]
    if field.lower() not in ("name", "phone"):
        return f"Unknown field '{field}'.\nTo see more info enter 'help'"
    ab = classes.AddressBook.open_file("data.csv")
    result = ab.search(field, text)
    if not result:
        return "There are no users matching"
    return "\n".join([str(rec) for rec in result])


@set_commands("exit", "close", "good bye")
@input_error
def exit(*args):
    """Interrupt program."""
    sys.exit(0)


@set_commands("address")
@input_error
def address(*args):
    """Take the input username and show the address"""
    name = classes.Name(args[0])

    data = classes.AddressBook.open_file("data.csv")
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


# Для того, щоб дадати нові команди до бота достатньо просто
# тут написати іх код з відповідними декораторами та docstring.
# Наприклад, уявімо, що потрібно додати команду, що повертатиме ввід користувача.
# Якщо розчоментувати кож нижче можна побачити, що команда echo працює успішно

# @set_commands("echo")
# @input_error
# def echo(*args):
#     """Return user`s input"""
#     return " ".join(args)