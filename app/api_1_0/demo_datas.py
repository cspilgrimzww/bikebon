# coding=utf-8
from ..models import BKUser,BKBike
from .. import db

def seed_user():
    user1 = BKUser(user_name=u'小肥', user_phone=u'10086',user_balance=500,user_deposit=23333)
    user2 = BKUser(user_name=u'浩宇', user_phone=u'10010',user_balance=500,user_deposit=23333)
    user3 = BKUser(user_name=u'小贤', user_phone=u'10000',user_balance=500,user_deposit=23333)
    user4 = BKUser(user_name=u'小娴', user_phone=u'110',user_balance=500,user_deposit=23333)
    user5 = BKUser(user_name=u'钟蔚蔚', user_phone=u'13056961943',user_confirmed = True,user_balance=500,user_deposit=23333)
    db.session.add_all([user1,user2,user3,user4,user5])
    db.session.commit()

def seed_bike():
    bike1 = BKBike(bike_status =u'空闲', bike_type = u'山地车', bike_rent_price = 5)
    bike2 = BKBike(bike_status =u'空闲', bike_type = u'公路车', bike_rent_price = 5)
    bike3 = BKBike(bike_status =u'空闲', bike_type = u'滑板车', bike_rent_price = 5)
    bike4 = BKBike(bike_status =u'空闲', bike_type = u'电动车', bike_rent_price = 5)
    db.session.add_all([bike1,bike2,bike3,bike4])
    db.session.commit()

