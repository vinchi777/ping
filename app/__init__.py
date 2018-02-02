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
    from app.models import Devise, TimeStamp

    @app.route('/<devise_id>/<int:epoch_time>', methods=['POST'])
    def create(devise_id, epoch_time):
        devise = Devise.save_ping(devise_id, epoch_time)
        response = jsonify({
            'id': devise.request_devise_id
            })

        response.status_code = 201
        return response

    @app.route('/<devise_id>/<from_date>', methods=['GET'])
    @app.route('/<devise_id>/<from_date>/<to_date>', methods=['GET'])
    def index(devise_id, from_date=None, to_date=None):
        results = []
        pings = TimeStamp.get_all(devise_id, from_date, to_date)

        if devise_id == 'all':
            obj = {}
            for ping in pings:
                obj[str(ping.devise.request_devise_id)] = obj.get(str(ping.devise.request_devise_id), [])
                obj[str(ping.devise.request_devise_id)].append(ping.ping_at.strftime('%s'))
            results = obj
        else:
            for ping in pings:
                obj = ping.ping_at.strftime('%s')
                results.append(obj)

        response = jsonify(results)
        response.status_code = 201

        return response

    @app.route('/devices', methods=['GET'])
    def devices():
        results = []
        devices = Devise.query.all()
        for device in devices:
            results.append(device.request_devise_id)

        response = jsonify(results)
        response.status_code = 201

        return response

    @app.route('/clear_data', methods=['POST'])
    def clear_data():
        db.session.query(TimeStamp).delete()
        db.session.query(Devise).delete()
        db.session.commit()

        response = jsonify({})
        response.status_code = 200

        return response


    return app
