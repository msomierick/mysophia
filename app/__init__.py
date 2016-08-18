from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
toolbar = DebugToolbarExtension()
login_manager.session_protection = 'strong'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    toolbar.init_app(app)

    from students import students as students_blueprint
    from app.main import main as main_blueprint
    app.register_blueprint(students_blueprint, url_prefix='/student')
    app.register_blueprint(main_blueprint, url_prefix='')
    return app
