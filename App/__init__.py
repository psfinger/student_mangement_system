import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()
bootstrap = Bootstrap()


def create_app(config_class=Config):
    BASE_DIR = os.path.dirname(__file__)
    static_dir = os.path.join(BASE_DIR, 'static')
    templates_dir = os.path.join(BASE_DIR, 'templates')

    app = Flask(__name__,
                static_folder=static_dir,
                template_folder=templates_dir)
    app.config.from_object(config_class)

    bootstrap.init_app(app)
    db.init_app(app=app)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from App.main import main_blueprint
    from App.user import user_blueprint

    app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')
    app.register_blueprint(blueprint=main_blueprint, url_prefix='/')
    app.add_url_rule('/', endpoint='main.home')

    return app
