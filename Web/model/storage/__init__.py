import typing

import bcrypt

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select

from model.storage.tables import *

class Storage:
    def __init__(self, config):
        db_type = config.get('db.type')
        connect_args = {}
        if db_type == 'file':
            conn_str = 'sqlite:///' + config.get('db.file')
            # TODO: try to avoid this, 
            # can cause database corruption if multiple writing operations exist
            connect_args['check_same_thread'] = False
        elif db_type == 'string':
            conn_str = config.get('db.conn_str')
        elif db_type == 'details':
            username = config.get('db.username')
            password = config.get('db.password')
            host = config.get('db.host')
            port = config.get('db.port')
            if port:
                host += ':' + port
            database = config.get('db.database')
            
            # Try to use db_type as dialect
            conn_str = f'{db_type}://{username}:{password}@{host}/{database}'
        else:
            return
        
        # Create sqlalchemy engine
        engine = create_engine(conn_str, connect_args=connect_args)

        # Create tables if non-existant
        Base.metadata.create_all(engine)

        # Create session
        self.session = sessionmaker(engine)()
    
    # Notes related methods
    def get_all_notes(self):
        return self.session.query(Note).all()
    
    def get_note(self, id: int):
        try:
            return self.session.query(Note).get(id)
        except Exception as e:
            self.session.rollback()
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
            self.session.rollback()
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
            self.session.rollback()
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
            self.session.rollback()
            print(e)
            return None

    # User related methods
    def get_user(self, username: str):
        try:
            return self.session.query(User).get(username)
        except Exception as e:
            self.session.rollback()
            print(e)
            return None

    def create_user(self, username: str, password: str):
        try:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            new_user = User(username=username, password=hashed_password)
            self.session.add(new_user)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(e)
            return False
