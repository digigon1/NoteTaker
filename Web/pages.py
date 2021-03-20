import http
import functools

from flask import Blueprint, jsonify, abort, request, session

from model import Model
from views import Views

def check_auth(func):
    @functools.wraps(func)
    def decorated(*args, **kwargs):
        user = session.get('user')
        if not user:
            return abort(http.client.UNAUTHORIZED)
        
        return func(*args, **kwargs)
    return decorated

class Pages():
    @staticmethod
    def create(config):
        pages = Blueprint('pages', __name__)

        @pages.route('/')
        @pages.route('/login/')
        def login():
            session['user'] = 'test'  # Debug
            return Views.get().login()

        @pages.route('/notes/')
        @check_auth
        def show_all_notes():
            results = Model.get().list_notes()
            return Views.get().list_notes(results)

        @pages.route('/notes/<int:note_id>')
        @check_auth
        def show_note(note_id: int):
            note = Model.get().get_note(note_id)
            if note:
                return Views.get().show_note(note)
            else:
                abort(http.client.NOT_FOUND)

        return pages

