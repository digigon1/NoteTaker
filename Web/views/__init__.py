from flask import render_template


class Views:
    __instance = None
    
    @classmethod
    def get(cls):
        return Views.__instance
    
    @classmethod
    def init(cls, config):
        Views.__instance = Views(config)

    def __init__(self, config):
        # No need for config yet, pass for consistency
        pass

    # Building pages
    def login(self):
        return render_template('login.html')

    def list_notes(self, notes):
        return render_template('notes.html', notes=notes)

    def show_note(self, note):
        return render_template('note.html', title=note.title, content=note.content)