from flask import render_template


class Views:
    def __init__(self, config):
        # No need for config yet, pass for consistency
        pass

    # Building pages
    def list_notes(self, notes):
        return render_template('notes.html', notes=notes)

    def show_note(self, note):
        return render_template('note.html', title=note.title, content=note.content)