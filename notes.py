from collections import UserList
import json
import re


class Note:
    def __init__(self, text):
        self.text = text

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


class NoteBook(UserList):
    # У полі all_keywords зберігаються унікальні ключові слова з усіх нотаток
    all_keywords = set()

    def add_note(self, note: None):
        self.append(note)
        self.all_keywords.update(note.keywords)

    def save_to_file(self):
        result = []
        for note in self.data:
            result.append(
                {
                    "tags": note.keywords,
                    "text": note.text
                }
            )
        with open("notebook.json", "w") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)

    @classmethod
    def read_from_file(cls):
        try:
            with open("notebook.json") as file:
                data_json = json.load(file)
                data = cls()
                for note in data_json:
                    data.add_note(Note(note["text"]))
        except FileNotFoundError:
            data = cls()
        return data
