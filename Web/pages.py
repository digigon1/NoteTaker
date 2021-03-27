import http
import functools

from flask import Blueprint, jsonify, abort, request, session, redirect

from model import Model
from views import Views
from security import JWT

def check_auth(func):
    @functools.wraps(func)
    def decorated(*args, **kwargs):
        try:
            token = session['token']
            if not token:
                return redirect('/')
        except Exception as _:
            return redirect('/')
        
        user = JWT.decode(token)
        if not user:
            return redirect('/')
        
        kwargs['user'] = user

        return func(*args, **kwargs)
    return decorated

class Pages():
    @staticmethod
    def create(config):
        pages = Blueprint('pages', __name__)

        @pages.route('/')
        @pages.route('/login/')
        def login():
            if 'token' in session:
                return redirect('/notes/')

            return Views.get().login()

        @pages.route('/logout/')
        @check_auth
        def logout(user: str):
            del session['token']
            return redirect('/')

        @pages.route('/notes/')
        @check_auth
        def show_all_notes(user: str):
            results = Model.get().list_notes(user)
            return Views.get().list_notes(results)

        @pages.route('/notes/<int:note_id>')
        @check_auth
        def show_note(note_id: int, user: str):
            note = Model.get().get_note(note_id, user)
            if note:
                return Views.get().show_note(note)
            else:
                abort(http.client.NOT_FOUND)

        return pages

