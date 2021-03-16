import sqlite3
import typing

from model.storage import Storage

class Model:
    def __init__(self, config):
        self.storage = Storage(config)

    # All notes functions
    def list_notes(self):
        return self.storage.get_all_notes()

    # Single note functions
    def get_note(self, note_id: int):
        return self.storage.get_note(note_id)
        
    def create_note(self, title: str):
        return self.storage.create_note(title)  # Returns new id
        
    def delete_note(self, note_id: int):
        result = self.storage.delete_note(note_id)
        if result == None:
            return None  # Propagate error
        else:
            return result != 0

    def update_note(self, note_id: int, title: typing.Optional[str], content: typing.Optional[str]):
        if not title and not content:
            return None  # Error, at least one must be updated

        return self.storage.update_note(note_id, title, content)