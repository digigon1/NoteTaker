import http

from flask import Flask, session
from flaskext.markdown import Markdown

from api import API
from pages import Pages

from views import Views
from model import Model
import config


# Setup
config.init()
api = API.create(config)  # REST interface
pages = Pages.create(config)  # Views

app = Flask('Note Taker')
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(pages)
Markdown(app)


# Run flask app
if __name__ == "__main__":
    debug = False
    
    if config.get('app.debug'):
        app.jinja_env.auto_reload = True
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        debug = True

    app.secret_key = 'secret_key'

    app.run(host='0.0.0.0', debug=debug)