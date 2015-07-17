__author__ = 'cspilgrim'
from itsdangerous import TimedJSONWebSignatureSerializer as Serialize
from . import db
from flask.ext.login import AnonymousUserMixin
from flask import current_app
from app.exceptions import ValidationError

class BKUser(db.Model):
    __tablename__ = 'bk_user'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), index=True)
    user_password_hash = db.Column(db.String(128))
    user_phone = db.Column(db.String(32))
    user_balance = db.Column(db.Float)
    user_deposit = db.Column(db.Float)

    def generate_auth_token(self,expiration):
        s = Serialize(current_app.config['SECRET_KEY'],
                      expires_in=expiration)
        return s.dumps({'id',self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serialize(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return BKUser.query.get(data['id'])

    def to_json(self):
        json_user = {
            'username':self.user_name,
            'phone':self.user_phone,
            'balance':self.user_balance,
            'deposit':self.user_deposit
        }
        return json_user

class BKBike(db.Model):
    __tablename__ = 'bk_bike'
    bike_id = db.Column(db.Integer,primary_key=True)
    bike_name = db.Column(db.String(32))
    bike_status = db.Column(db.String(32))
    bike_rent_price = db.Column(db.Float)
    bike_type = db.Column(db.String(32))
    user = db.Column(db.Integer,db.ForeignKey('bk_user.user_id'))

    def to_json(self):
        bike_json={
            'id': self.bike_id,
            'name': self.bike_name,
            'status': self.bike_status,
            'price': self.bike_rent_price,
            'type': self.bike_type
        }
        return bike_json

    @staticmethod
    def from_json(json_bike):
        id = json_bike.get('id')
        if id is None or id =='':
            raise ValidationError(u'')
        name = json_bike.get('name')
        status = json_bike.get('status')
        price = json_bike.get('price')
        type = json_bike.get('type')
        user = json_bike.get('user')
        return BKBike(bike_id = id, bike_name = name, bike_status = status,
                      bike_price = price, bike_type = type, bike_user = user)

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False