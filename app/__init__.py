from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.errors import bp as bp_errors
    app.register_blueprint(bp_errors)

    from app.main import bp as bp_main
    app.register_blueprint(bp_main)

    return app


from app import models
