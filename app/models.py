#coding=utf-8
__author__ = 'cspilgrim'
from itsdangerous import TimedJSONWebSignatureSerializer as Serialize
from . import db
from flask.ext.login import AnonymousUserMixin
from flask import current_app
from app.exceptions import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash

class Status():
    LOCKED = u'待取'
    AVAILABLE = u'待租'
    USING = u'使用中'

class Login_status():
    LOGIN = u"登陆状态"
    LOGOUT = u"登出状态"

class BKUser(db.Model):
    __tablename__ = 'bk_user'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), index=True)
    user_phone = db.Column(db.String(32))
    user_password_hash = db.Column(db.String(128))
    user_identity_number = db.Column(db.String(32), unique= True)
    user_student_identity_number = db.Column(db.String(32), unique= True)
    user_current_token = db.Column(db.Integer)
    user_balance = db.Column(db.Float,default=0)
    user_deposit = db.Column(db.Float,default=0)
    user_verify = db.Column(db.Boolean,default=False)
    user_confirmed = db.Column(db.Boolean,default=False)

    @property
    def is_anonymous(self):
        return self.user_phone is None

    @property
    def password(self):
        raise AttributeError(u'密码散列值是不可读属性')

    @password.setter
    def password(self, password):
        self.user_password_hash = generate_password_hash(password)

    def verify_password(self, password):
        verify_result=check_password_hash(self.user_password_hash,password)
        print("user_password_hash_result:"+str(verify_result))
        return check_password_hash(self.user_password_hash,password)



    def generate_auth_token(self,expiration):
        s = Serialize(current_app.config['SECRET_KEY'],
                      expires_in=expiration)
        return s.dumps({'user_phone':self.user_phone})

    @staticmethod
    def verify_auth_token(token):
        s = Serialize(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return BKUser.query.filter_by(user_phone=data['user_phone']).first()

    def to_json(self):
        json_user = {
            'username':self.user_name,
            'phone':self.user_phone,
            'balance':self.user_balance,
            'deposit':self.user_deposit,
            'confirm_info': self.user_verify
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
