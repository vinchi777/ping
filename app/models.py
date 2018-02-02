from app import db
from datetime import datetime, date
from sqlalchemy import cast, DATE
import re

class Devise(db.Model):

    __tablename__ = 'devises'

    id = db.Column(db.Integer, primary_key=True)
    request_devise_id = db.Column(db.String(128), index=True, unique=True)
    time_stamps = db.relationship('TimeStamp', backref='devise', lazy='dynamic')

    @staticmethod
    def save_ping(devise_id, epoch_time):
        formated_time = datetime.utcfromtimestamp(epoch_time)
        devise = Devise.query.filter_by(request_devise_id=devise_id).first()

        if devise is None: devise = Devise(request_devise_id=devise_id)

        timestamp = TimeStamp(ping_at=formated_time)
        devise.time_stamps.append(timestamp)
        db.session.add(devise)
        db.session.commit()
        return devise


    def __repr__(self):
        return '<Devise: {}>'.format(self.request_devise_id)


class TimeStamp(db.Model):

    __tablename__ = 'time_stamps'

    id = db.Column(db.Integer, primary_key=True)
    devise_id = db.Column(db.Integer, db.ForeignKey('devises.id'))
    ping_at = db.Column(db.DateTime(timezone=True))

    @staticmethod
    def get_all(devise_id, from_date, to_date):
        result = None

        if devise_id != 'all':
            devise = Devise.query.filter_by(request_devise_id=devise_id).first()
            if devise is None: return []
            query = TimeStamp.single_or_range_query(from_date, to_date)
            result = query.filter(TimeStamp.devise_id == devise.id).all()
        else:
            query = TimeStamp.single_or_range_query(from_date, to_date)
            result = query.all()

        return result


    @staticmethod
    def convert_to_datetime(date_str):
        if re.match('^\d{4}-\d{2}-\d{2}$', date_str):
            result = datetime.strptime(date_str, '%Y-%m-%d')
        else:
            # result = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(date_str)))
            result = datetime.utcfromtimestamp(float(date_str))

        return result

    @staticmethod
    def date_range_query(start_date, end_date):
        query = TimeStamp.query \
                .filter(TimeStamp.ping_at >= start_date) \
                .filter(TimeStamp.ping_at < end_date)
        return query

    @staticmethod
    def single_date_query(start_date):
        query = TimeStamp.query.filter(cast(TimeStamp.ping_at, DATE) == start_date.date())
        return query

    @staticmethod
    def single_or_range_query(from_date, to_date):
        if to_date is None:
            start_date = datetime.strptime(from_date, '%Y-%m-%d')
            query = TimeStamp.single_date_query(start_date)
        else:
            start_date = TimeStamp.convert_to_datetime(from_date)
            end_date = TimeStamp.convert_to_datetime(to_date)
            query = TimeStamp.date_range_query(start_date, end_date)
        return query

    def __repr__(self):
        return '<TimeStamp: {}>'.format(self.id)

