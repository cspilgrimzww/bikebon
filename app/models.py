#coding=utf-8
__author__ = 'cspilgrim'
from itsdangerous import TimedJSONWebSignatureSerializer as Serialize
from . import db
from flask.ext.login import AnonymousUserMixin
from flask import current_app,url_for
from app.exceptions import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

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
    user_current_token = db.Column(db.String(32))
    user_balance = db.Column(db.Float,default=0)
    user_deposit = db.Column(db.Float,default=0)
    user_verify = db.Column(db.Boolean,default=False)
    user_confirmed = db.Column(db.Boolean,default=False)
    user_gender = db.Column(db.String(32))
    user_school=db.Column(db.String(64))
    user_login_status=db.Column(db.String(32))
    user_bike_type_comments = db.relationship("BKBikeTypeComments", backref="owner", lazy="dynamic")


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
        print data['user_phone']
        return BKUser.query.filter_by(user_phone=data['user_phone']).first()

    def to_json(self):
        json_user = {
            'username':self.user_name,
            'gender':self.user_gender,
            'school':self.user_school,
            'phone':self.user_phone,
            'balance':self.user_balance,
            'deposit':self.user_deposit,
            'verify_info': self.user_verify,
        }
        return json_user

class BKBike(db.Model):
    __tablename__ = 'bk_bike'
    bike_id = db.Column(db.Integer,primary_key=True)
    bike_name = db.Column(db.String(32))
    bike_status = db.Column(db.String(32))
    bike_rent_price = db.Column(db.Float)
    bike_type = db.Column(db.String(32), db.ForeignKey('bk_bike_type.bike_type_id'))#定义外键，与车型相关联
    bike_user = db.Column(db.Integer, db.ForeignKey('bk_user.user_id')) #定义外键，与租车用户关联
    bike_description=db.Column(db.Text)
    bike_lender_id = db.Column(db.Integer, db.ForeignKey('bk_lender.lender_id')) #定义外键，与租车方联系

    def to_json(self):
        bike_json = {
            'id': self.bike_id,
            'name': self.bike_name,
            'status': self.bike_status,
            'price': self.bike_rent_price,
            'type': self.bike_type,
            'description':self.bike_description
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
        desc=json_bike.get('description')
        return BKBike(bike_id = id, bike_name = name, bike_status = status,
                      bike_price = price, bike_type = type, bike_user = user,bike_description=desc)

#车型
class BKBikeType(db.Model):
    __tablename__ = 'bk_bike_type'
    bike_type_id = db.Column(db.Integer,primary_key=True)
    bike_type_name = db.Column(db.String(32))
    bike_type_price = db.Column(db.String(32))
    bike_type_description = db.Column(db.Text)
    bikes = db.relationship("BKBike",backref="type_of", lazy ="dynamic")

    def to_json(self):
        bike_type_json = {
            "id":self.bike_type_id,
            "name":self.bike_type_name,
            "price":self.bike_type_price,
            "description":self.bike_type_description
        }
        return bike_type_json

#订单模型
class BKOrder(db.Model):
    __tablename__= 'bk_order'
    order_id = db.Column(db.Integer,primary_key=True)
    order_price = db.Column(db.Float)
    order_time = db.Column(db.String(64))
    order_form_status= db.Column(db.String(64),index=True)
    belong_to = db.Column(db.Integer,db.ForeignKey('bk_user.user_id')) #定义外键，与租车用户联系


    def to_json(self):
        order_json={
            'id':self.order_id,
            'price':self.order_price,
            'time':self.order_time,
            'status':self.order_form_status
        }
        return order_json

    @staticmethod
    def from_json(json_order):
        id = json_order.get('id')
        if id is None or id =='':
            raise ValidationError(u'')
        price = json_order.get('price')
        time=json_order.get('time')
        status=json_order.get('status')

        return BKOrder(order_id=id,order_price=price,order_time=time,order_status=status)




#商家模型
class BKLender(db.Model):
    __tablename__ = 'bk_lender'
    lender_id = db.Column(db.Integer,primary_key=True)
    lender_account = db.Column(db.Float)
    lender_description = db.Column(db.Text)
    lender_position = db.Column(db.String(64),index=True)
    lender_notice = db.Column(db.String(128))  #公告
    bike = db.relationship('BKBike', backref='lender') #定义和BKBike的关系，从BKbike中可返回属于某个商家的全部自行车列表


    def to_json(self):
        lender_json={
            'id':self.lender_id,
            'account':self.lender_account,
            'description':self.lender_description,
            'notice':self.lender_notice,
            'position':self.lender_position
        }
        return lender_json


    @staticmethod
    def from_json(json_lender):
        id = json_lender.get('id')
        if id is None or id =='':
            raise ValidationError(u'')
        account=json_lender.get('account')
        position=json_lender.get('position')
        notice=json_lender.get('notice')
        desc=json_lender.get('description')
        return BKLender(lender_id=id,lender_account=account,lender_position=position,lender_notice=notice,
                        lender_description=desc)

class BKBikeTypeComments(db.Model):
    __tablename__='bk_bike_type_comments'
    bike_type_comments_id = db.Column(db.Integer,primary_key=True)
    bike_type_comments_body = db.Column(db.Text)
    bike_type_comments_user_id = db.Column(db.Integer, db.ForeignKey("bk_user.user_id"))
    bike_type_comments_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    bike_type_comments_bike_type = db.Column(db.Integer,db.ForeignKey("bk_bike_type.bike_type_id"))

    def to_json(self):
        json_comments={
            "id":self.bike_type_comments_id,
            "body":self.bike_type_comments_body,
            "user_id":self.bike_type_comments_user_id,
            "time":self.bike_type_comments_timestamp
        }
        return json_comments

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

class BKHeadImg(db.Column):
    __tablename__ = "bk_head_image"
    head_image_id = db.Column(db.Integer, primary_key=True)
    head_image_name = db.Column(db.String(128))
    head_image_path = db.Column(db.String(128))
    head_image_status = db.Column(db.Boolean, default=False)

    def to_json(self):
        json_img = {
            "name": self.head_image_name,
            "path": self.head_image_path
        }
        return json_img