import typing

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select

from model.storage.tables import *

class Storage:
    def __init__(self, config):
        if config.get('db.type') == 'file':
            conn_str = 'sqlite:///' + config.get('db.file')
        else:
            conn_str = ''  # Not implemented yet
        
        # Create sqlalchemy engine
        engine = create_engine(conn_str)

        # Create tables if non-existant
        Base.metadata.create_all(engine)

        # Create session
        self.session = sessionmaker(engine)()
    
    def get_all_notes(self):
        return self.session.query(Note).all()
    
    def get_note(self, id: int):
        try:
            return self.session.query(Note).get(id)
        except Exception as e:
            print(e)
            return None

    def create_note(self, title: str):
        try:
            new_note = Note(title=title)
            self.session.add(new_note)
            self.session.flush()  # Make note be stored
            self.session.refresh(new_note)  # Get stored id
            new_id = new_note.id
            self.session.commit()
            return new_id
        except Exception as e:
            print(e)
            return None

    def delete_note(self, id: int):
        try:
            note = self.session.query(Note).get(id)
            if note:
                self.session.delete(note)
                self.session.commit()
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return None
    
    def update_note(self, id: int, title: typing.Optional[str], content: typing.Optional[str]):
        try:
            note = self.session.query(Note).get(id)
            if not note:
                return False

            if title:
                note.title = title

            if content:
                note.content = content

            self.session.commit()
            return True
        except Exception as e:
            print(e)
            return None
