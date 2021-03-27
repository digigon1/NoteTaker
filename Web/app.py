import http

from flask import Flask, session
from flaskext.markdown import Markdown

from api import API
from pages import Pages

from views import Views
from model import Model
from security import JWT
import config


# Setup
config.init()

Model.init(config)
Views.init(config)
JWT.init(config)

app = Flask('Note Taker')

api = API.create(config)  # REST interface
app.register_blueprint(api, url_prefix='/api')

pages = Pages.create(config)  # Views
app.register_blueprint(pages)

Markdown(app)


# Run flask app
if __name__ == "__main__":
    # Setup debug option
    debug = False
    if config.get('app.debug'):
        app.jinja_env.auto_reload = True
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        debug = True

    # Setup sessions
    secret_key = config.get('app.secret_key')
    if not secret_key:
        secret_key = 'secret_key'
    app.secret_key = secret_key

    # Setup https and launch
    https_support = config.get('app.https_mode')
    if not https_support:
        app.run(host='0.0.0.0', debug=debug)
    elif https_support == 'adhoc':
        app.run(host='0.0.0.0', debug=debug, ssl_context='adhoc')
    elif https_support == 'cert':
        cert = config.get('app.cert')
        if cert:
            app.run(host='0.0.0.0', debug=debug, ssl_context=(cert.cert, cert.key))
        else:
            # Try with default names
            app.run(host='0.0.0.0', debug=debug, ssl_context=('cert.pem', 'key.pem'))
    else:
        # Just launch without https
        app.run(host='0.0.0.0', debug=debug)