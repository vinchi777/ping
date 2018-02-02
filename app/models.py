from app import db

class Devise(db.Model):

    __tablename__ = 'devises'

    id = db.Column(db.Integer, primary_key=True)
    request_devise_id = db.Column(db.String(128), index=True, unique=True)
    time_stamps = db.relationship('TimeStamp', backref='devise', lazy='dynamic')

    def __repr__(self):
        return '<Devise: {}>'.format(self.request_devise_id)


class TimeStamp(db.Model):

    __tablename__ = 'time_stamps'

    id = db.Column(db.Integer, primary_key=True)
    devise_id = db.Column(db.Integer, db.ForeignKey('devises.id'))

    def __repr__(self):
        return '<TimeStamp: {}>'.format(self.id)

