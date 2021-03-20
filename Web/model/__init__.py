import typing

from model.storage import Storage

_instance = None

class Model:
    @classmethod
    def get(cls):
        global _instance
        return _instance
    
    @classmethod
    def init(cls, config):
        global _instance
        _instance = Model(config)

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

    # User related functions
    def get_user(self, username: str):
        return self.storage.get_user(username)

    def create_user(self, username: str, password: str):
        return self.storage.create_user(username, password)