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
        return f"{self.id}: {self.text}"

    def __repr__(self):
        return str(self)


class NoteBook(UserDict):
    def __add__(self, other):
        if isinstance(other, NoteBook):
            new_notebook = NoteBook()
            new_notebook.update(self.data)
            new_notebook.update(other.data)
            return new_notebook
        else:
            raise TypeError("Can only add two NoteBook instances together")

    def add_note(self, text: str):
        note_id = str(random.randint(1000, 9999))
        note = Note(text, note_id)
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

    def find_notes_by_keyword(self, keyword):
        result = []
        for note in self.data.values():
            if keyword in note.tags:
                result.append(str(note))
        if not result:
            return "There are no notes matching"
        return "\n".join(result)

    def find_notes_by_text(self, text):
        result = []
        for note in self.data.values():
            if text in note.text:
                result.append(str(note))
        if not result:
            return "There are no notes matching"
        return "\n".join(result)

    def sort_notes(self, keyword):
        notes_with_keyword = NoteBook()
        notes_without_keyword = NoteBook()
        nb = NoteBook.read_from_file()

        for note in nb.data.values():
            if keyword.lower() in note.tags:
                notes_with_keyword[note.id] = note
            else:
                notes_without_keyword[note.id] = note

        if not notes_with_keyword:
            return f"Keyword {keyword} not found"

        return notes_with_keyword + notes_without_keyword

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
