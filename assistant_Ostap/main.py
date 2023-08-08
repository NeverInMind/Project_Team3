import logging
import re

from fuzzywuzzy import fuzz, process
import readline

import classes
from assistant_Ostap.handlers import commands
from assistant_Ostap.notes import NoteBook


# Даний метод відповідає за автозаповнення команд. Якщо у консолі
# ввести частину команди та натиснути tab то команда доповниться.
# у разі, якщо більше однієї команди відповідають критеріям,
# повернеться список усіх доступних команд
def completer(text, state):
    if not text.isalpha():
        return None
    options = [cmd for cmd in commands.keys() if cmd.startswith(text.lower())]
    if not options:
        return None
    if state < len(options):
        return options[state]
    return None


def parse_command(user_input: str):
    # Даний регулярний вираз шукає команди, що складаються більше, ніж з одного слова.
    # Тобто це good bye, show all, del phone та del user.
    # Якщо користувач ввів одну із цих команд, командою вважатимуться перші два слова,
    # а аргументами - все, починаючи з третього. Я
    # кщо ж команда складаєтсья з одного слова(блок else),
    # то аргументами є все, починаючи з другого елементу
    match = re.search(
        r"^show\s|^good\s|^del\s", user_input.lower())
    try:
        if match:
            user_command = " ".join(user_input.split()[:2]).lower()
            command_arguments = user_input.split()[2:]
        else:
            user_command = user_input.split()[0].lower()
            command_arguments = user_input.split()[1:]
    except IndexError:
        return "Please enter a command name."

    # Тут обробляються випадки, коли користувач ввів нвідому команду.
    # Якщо ввід схожий на існуючу команду, наприклад, chanle, то
    # повернеться повідомлення: "Можливо Ви мали на увазі change"
    # Якщо ж жодна із команд не буде достатньо подібною до
    # вводу користувача(за це відповідає змінна match_ratio
    # та коефіцієнт 60, виведений експерементальним шляхом),
    # повернеться повідомлення про те що команду не знайдено.
    if user_command not in commands.keys():
        logging.basicConfig(level=logging.ERROR)
        best_match, match_ratio = process.extractOne(user_command,
                                                     commands.keys(),
                                                     scorer=fuzz.ratio)
        if match_ratio >= 60:
            return f"Command not found.\nPerhaps you meant '{best_match}'."
        else:
            return "Command not found.\nTo view all available commands, enter 'help'."
    else:
        return commands[user_command](*command_arguments)


def main():
    # Ці дві лінійки безпосередньо пов'язані з функцією completer.
    # Вони відповідають за те, при натисканні на яку кнопку відбуватиметься автодоповнення.
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

    while True:
        user_input = input("Enter command: ")
        result = parse_command(user_input)

        if result:
            # Якщо повернули ітератор(тобто команда show all), проходимося по ньому в циклі,
            #  поступово показуючи записи
            if isinstance(result, classes.AddressBook) or isinstance(result, NoteBook):
                for page in result:
                    commands["clear"]()
                    print("\n".join([str(i) for i in page]))
                    user_input = input(
                        "Press 'q' to quit. Press any key to see the next page: ")
                    if user_input.lower() == "q":
                        break
            else:
                print(result)


if __name__ == "__main__":
    main()
