from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import app_config

import logging

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)

    migrate = Migrate(app, db)
    from app import models


    @app.route('/<devise_id>/<epoch_time>', methods=['POST'])
    def create(devise_id, epoch_time):
        app.logger.info(devise_id)
        app.logger.info(epoch_time)
        app.logger.info(models.Ping)
        return 'Hello World'


    return app
