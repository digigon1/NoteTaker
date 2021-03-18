import http

from flask import Flask, request, abort, redirect, jsonify
from flaskext.markdown import Markdown

from views import Views
from model import Model
import config


# Setup
config.init()
app = Flask('Note Taker')
Markdown(app)
model = Model(config)
views = Views(config)



# Views
@app.route('/')
def root():
    return redirect('/notes/')

@app.route('/notes/')
def show_all_notes():
    results = model.list_notes()
    return views.list_notes(results)

@app.route('/notes/<int:note_id>')
def show_note(note_id: int):
    note = model.get_note(note_id)
    if note:
        return views.show_note(note)
    else:
        abort(http.client.NOT_FOUND)


# REST interface
# Note related endpoints
@app.route('/api/notes/', methods=['GET'])
def list_notes():
	result = model.list_notes()
	return (jsonify(result), http.client.OK)

@app.route('/api/notes/', methods=['PUT'])
def create_note():
    if request.form and request.form['title']:
        new_id = model.create_note(request.form['title'])

        if new_id != None:
            return (str(new_id), http.client.OK)
        else:
            return abort(http.client.INTERNAL_SERVER_ERROR)
    else:
        return abort(http.client.BAD_REQUEST, message='Missing title')

@app.route('/api/notes/<int:note_id>', methods=['GET'])
def get_note(note_id: int):
    result = model.get_note(note_id)

    if result:
        return result
    else:
        abort(http.client.NOT_FOUND)
    
@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id: int):
    result = model.delete_note(note_id)

    if result == None:
        return abort(http.client.INTERNAL_SERVER_ERROR)

    if result == False:
        return abort(http.client.NOT_FOUND)

    return ('', http.client.NO_CONTENT)

@app.route('/api/notes/<int:note_id>', methods=['POST'])
def update_note(note_id: int):
    if not request.form:
        abort(http.client.BAD_REQUEST)

    if not request.form['title'] and not request.form['content']:
        abort(http.client.BAD_REQUEST, message='No changes given')

    result = model.update_note(note_id, request.form['title'], request.form['content'])

    if result == None:
        return abort(http.client.INTERNAL_SERVER_ERROR)

    if result == False:
        return abort(http.client.NOT_FOUND)

    return ('', http.client.NO_CONTENT)

# User related endpoints
@app.route('/api/users/', methods=['PUT'])
def create_user():
    if request.form and request.form['username'] and request.form['password']:
        if model.create_user(request.form['username'], request.form['password']):
            return ('', http.client.NO_CONTENT)
        else:
            return abort(http.client.INTERNAL_SERVER_ERROR)
    else:
        return abort(http.client.BAD_REQUEST, message='Missing username and/or password')

# Authentication related endpoints
@app.route('/api/auth/', methods=['POST'])
def authenticate():
    if request.form and request.form['username'] and request.form['password']:
        user = model.get_user(request.form['username'])
        if user:
            if user.check_password(request.form['password']):
                # TODO: store user authentication somehow
                pass
            else:
                return abort(http.client.UNAUTHORIZED, message='Wrong username or password')
        else:
            return abort(http.client.UNAUTHORIZED, message='Wrong username or password')
    else:
        return abort(http.client.BAD_REQUEST, message='Missing username and/or password')

# Run flask app
if __name__ == "__main__":
    debug = False
    
    if config.get('app.debug'):
        app.jinja_env.auto_reload = True
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        debug = True

    app.run(host='0.0.0.0', debug=debug)