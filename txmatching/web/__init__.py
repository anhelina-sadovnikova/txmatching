import logging
import sys
from importlib import util as importing

import flask_login
from flask import Flask
from flask_restx import Api
from werkzeug.middleware.proxy_fix import ProxyFix

from txmatching.database.db import db
from txmatching.database.services.app_user_management import \
    get_app_user_by_email
from txmatching.web.api.auth_api import user_api
from txmatching.web.app_configuration.application_configuration import (
    ApplicationConfiguration, get_application_configuration)
from txmatching.web.auth import bcrypt
from txmatching.web.data_api import data_api
from txmatching.web.functional_api import functional_api
from txmatching.web.service_api import service_api

LOGIN_MANAGER = None


def create_app():
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s] - %(levelname)s - %(module)s: %(message)s',
                        stream=sys.stdout)

    app = Flask(__name__)
    # fix for https swagger - see https://github.com/python-restx/flask-restx/issues/58
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_port=1, x_for=1, x_host=1, x_prefix=1)

    # register blueprints
    app.register_blueprint(service_api)
    app.register_blueprint(functional_api)
    app.register_blueprint(data_api)

    # For flask.flash (gives feedback when uploading files)
    app.secret_key = 'secret key'

    # Add config
    app.config['CSV_UPLOADS'] = 'txmatching/web/csv_uploads'
    app.config['ALLOWED_FILE_EXTENSIONS'] = ['CSV', 'XLSX']

    global LOGIN_MANAGER
    LOGIN_MANAGER = flask_login.LoginManager()
    LOGIN_MANAGER.init_app(app)
    LOGIN_MANAGER.login_view = 'service.login'

    @LOGIN_MANAGER.user_loader
    def user_loader(user_id):
        return get_app_user_by_email(user_id)

    def load_local_development_config():
        config_file = 'txmatching.web.local_config'
        if importing.find_spec(config_file):
            app.config.from_object(config_file)

    def configure_db(application_config: ApplicationConfiguration):
        app.config['SQLALCHEMY_DATABASE_URI'] \
            = f'postgresql+psycopg2://' \
              f'{application_config.postgres_user}:{application_config.postgres_password}@' \
              f'{application_config.postgres_url}/{application_config.postgres_db}'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.init_app(app)

    def configure_encryption():
        bcrypt.init_app(app)

    def configure_apis():
        # Set up Swagger and API
        authorizations = {
            'bearer': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization'
            }
        }

        api = Api(app, authorizations=authorizations, doc='/doc/')
        api.add_namespace(user_api, path='/user')

    with app.app_context():
        load_local_development_config()
        application_config = get_application_configuration()
        configure_db(application_config)
        configure_encryption()
        configure_apis()
        return app
