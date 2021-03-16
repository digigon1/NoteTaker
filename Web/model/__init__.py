import sqlite3
import typing


class Model:
    def __init__(self, config):
        # TODO: add sqlalchemy support for easy multiple databases
        self.con = sqlite3.connect(config.get('db.file'), check_same_thread=False)

        cur = self.con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS notes (title text NOT NULL, content text DEFAULT '')")
        cur.close()

    # All notes functions
    def list_notes(self):
        cur = self.con.cursor()
        cur.execute('SELECT rowid, title FROM notes')
        results = [{'note_id': a[0], 'title': a[1]} for a in cur.fetchall()]
        cur.close()
        return results

    # Single note functions
    def get_note(self, note_id: int):
        try:
            cur = self.con.cursor()
            cur.execute('SELECT title, content FROM notes WHERE rowid = ?', (note_id, ))
            result = cur.fetchone()
            cur.close()
            return {'title': result[0], 'content': result[1]}
        except Exception as e:
            print(e)
            self.con.rollback()
            return None
        
    def create_note(self, title: str):
        try:
            cur = self.con.cursor()
            cur.execute('INSERT INTO notes(title) VALUES (?)', (title, ))
            self.con.commit()
            return cur.lastrowid
        except Exception as e:
            print(e)
            self.con.rollback()
            return None
        
    def delete_note(self, note_id: int):
        try:
            cur = self.con.cursor()
            cur.execute('DELETE FROM notes WHERE rowid = ?', (note_id, ))
            if cur.rowcount != 0:
                self.con.commit()
                cur.close()
                return True
            else:
                self.con.rollback()
                return False
        except Exception as e:
            print(e)
            self.con.rollback()
            return None

    def update_note(self, note_id: int, title: typing.Optional[str], content: typing.Optional[str]):
        try:
            cur = self.con.cursor()
            if title:
                cur.execute('UPDATE notes SET title = ? WHERE rowid = ?', (title, note_id))
                if cur.rowcount == 0:
                    return False
            
            if content:
                cur.execute('UPDATE notes SET content = ? WHERE rowid = ?', (content, note_id))
                if cur.rowcount == 0:
                    return False
            
            self.con.commit()
            return True
        except Exception as e:
            print(e)
            self.con.rollback()
            return None