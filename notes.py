from collections import UserDict
from dataclasses import dataclass, asdict
import json
import random
import re

import readline


@dataclass
class Note:
    text: str
    id: str
    tags: list = list

    def __post_init__(self):
        self.tags = self.keywords

    @property
    def keywords(self) -> list:
        # Ключовим вважається слово, перед яким у тексті є знак "#"
        pattern = r"#(\w+)"
        tags = re.findall(pattern, self.text.lower())
        return tags

    def __str__(self):
        return self.text

    def __repr__(self):
        return str(self)


class NoteBook(UserDict):
    # У полі all_keywords зберігаються унікальні ключові слова з усіх нотаток
    all_keywords = set()

    def add_note(self, text: str):
        note_id = str(random.randint(1000, 9999))
        note = Note(text, note_id)
        self.all_keywords.update(note.keywords)
        self.data[note_id] = note

    def edit_note(self, note_id):
        def set_initial_input(text):
            def hook():
                readline.insert_text(text)
                readline.redisplay()
            readline.set_pre_input_hook(hook)

        set_initial_input(self.data[note_id].text)
        user_input = input()
        new_note = Note(user_input, id=note_id)
        self.data[note_id] = new_note
        set_initial_input("")

    def del_note(self, note_id):
        del self[note_id]

    def save_to_file(self):
        result = {}
        for note_id, note in self.data.items():
            result[str(note_id)] = asdict(note)

        with open("notebook.json", "w") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)

    @classmethod
    def read_from_file(cls):
        try:
            with open("notebook.json") as file:
                data_json = json.load(file)
                data = cls()
                for note_json in data_json.values():
                    note = Note(**note_json)
                    data[note.id] = note

        except FileNotFoundError:
            data = cls()
        return data


if __name__ == "__main__":
    nb = NoteBook.read_from_file()
    print(nb)
