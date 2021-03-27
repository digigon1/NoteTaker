import http
import functools

from flask import Blueprint, jsonify, abort, request, session, make_response
import jwt

from model import Model
from security import JWT

def check_auth(func):
    @functools.wraps(func)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            token = request.headers['Authorization']
            if not token:
                return abort(http.client.UNAUTHORIZED)
        
        # TODO: extend verification based on user
        user = JWT.decode(token)
        if not user:
            return abort(http.client.UNAUTHORIZED)

        kwargs['user'] = user

        return func(*args, **kwargs)
    return decorated

class API():
    @staticmethod
    def create(config):
        api = Blueprint('api', __name__)

        # Note related endpoints
        @api.route('/notes/', methods=['GET'])
        @check_auth
        def list_notes(user):
            result = Model.get().list_notes(user)
            return (jsonify(result), http.client.OK)

        @api.route('/notes/', methods=['PUT'])
        @check_auth
        def create_note(user):
            if request.form and request.form['title']:
                new_id = Model.get().create_note(request.form['title'], user)

                if new_id != None:
                    return (str(new_id), http.client.OK)
                else:
                    return abort(http.client.INTERNAL_SERVER_ERROR)
            else:
                return abort(http.client.BAD_REQUEST, message='Missing title')

        @api.route('/notes/<int:note_id>', methods=['GET'])
        @check_auth
        def get_note(note_id: int, user):
            result = Model.get().get_note(note_id, user)

            if result:
                return result
            else:
                abort(http.client.NOT_FOUND)
            
        @api.route('/notes/<int:note_id>', methods=['DELETE'])
        @check_auth
        def delete_note(note_id: int, user):
            result = Model.get().delete_note(note_id, user)

            if result == None:
                return abort(http.client.INTERNAL_SERVER_ERROR)

            if result == False:
                return abort(http.client.NOT_FOUND)

            return ('', http.client.NO_CONTENT)

        @api.route('/notes/<int:note_id>', methods=['POST'])
        @check_auth
        def update_note(note_id: int, user):
            if not request.form:
                abort(http.client.BAD_REQUEST)

            if not request.form['title'] and not request.form['content']:
                abort(http.client.BAD_REQUEST, message='No changes given')

            result = Model.get().update_note(note_id, user, request.form['title'], request.form['content'])

            if result == None:
                return abort(http.client.INTERNAL_SERVER_ERROR)

            if result == False:
                return abort(http.client.NOT_FOUND)

            return ('', http.client.NO_CONTENT)

        # User related endpoints
        @api.route('/users/', methods=['PUT'])
        def create_user():
            if request.form and request.form['username'] and request.form['password']:
                if Model.get().create_user(request.form['username'], request.form['password']):
                    return ('', http.client.NO_CONTENT)
                else:
                    return abort(http.client.INTERNAL_SERVER_ERROR)
            else:
                return abort(http.client.BAD_REQUEST, message='Missing username and/or password')

        # Authentication related endpoints
        @api.route('/auth/', methods=['POST'])
        def authenticate():
            if request.form and request.form['username'] and request.form['password']:
                user = Model.get().get_user(request.form['username'])
                if user:
                    if user.check_password(request.form['password'].encode('utf-8')):
                        token = JWT.encode(user.username)
                        response = make_response(token, http.client.OK)
                        response.set_cookie('token', token)
                        session['token'] = token
                        return response
                    else:
                        return abort(http.client.UNAUTHORIZED, message='Wrong username or password')
                else:
                    return abort(http.client.UNAUTHORIZED, message='Wrong username or password')
            else:
                return abort(http.client.BAD_REQUEST, message='Missing username and/or password')

        return api