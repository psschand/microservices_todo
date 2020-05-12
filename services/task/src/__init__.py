import os
from flask import jsonify
from flask import Flask
from flask_cors import CORS
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from src.exceptions import APIException

# instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
toolbar = DebugToolbarExtension()


def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__)

    # set config
    # app_settings = os.getenv('APP_SETTINGS')
    # app.config.from_object(app_settings)
    app.config.from_object('src.config.BaseConfig')
    app.config.from_object('src.config.DevelopmentConfig')
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  
    # app.config['SQLALCHEMY_DATABASE_URI'] ="postgresql://postgres:postgres@192.168.99.100:5436/tasks"

    # set up extensions
    cors.init_app(app)
    toolbar.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from src.views.task import tasks_blueprint
    app.register_blueprint(tasks_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {
            'app': app,
            'db': db
        }

    @app.errorhandler(APIException)
    def generic_api_error_handler(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    return app
