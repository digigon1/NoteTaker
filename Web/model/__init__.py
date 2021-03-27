import typing

from model.storage import Storage

class Model:
    __instance = None
    
    @classmethod
    def get(cls) -> 'Model':
        return Model.__instance
    
    @classmethod
    def init(cls, config):
        Model.__instance = Model(config)

    def __init__(self, config):
        self.storage = Storage(config)

    # All notes functions
    def list_notes(self, user):
        return self.storage.get_all_notes(user)

    # Single note functions
    def get_note(self, note_id: int, user):
        return self.storage.get_note(note_id, user)
        
    def create_note(self, title: str, creator: str):
        return self.storage.create_note(title, creator)  # Returns new id
        
    def delete_note(self, note_id: int, user: str):
        result = self.storage.delete_note(note_id, user)
        if result == None:
            return None  # Propagate error
        else:
            return result != 0

    def update_note(self, note_id: int, user: str, title: typing.Optional[str], content: typing.Optional[str]):
        if not title and not content:
            return None  # Error, at least one must be updated

        return self.storage.update_note(note_id, user, title, content)

    # User related functions
    def get_user(self, username: str):
        return self.storage.get_user(username)

    def create_user(self, username: str, password: str):
        return self.storage.create_user(username, password)