#coding=utf-8
__author__ = 'cspilgrim'
from flask.ext.httpauth import HTTPBasicAuth
from .errors import forbidden, unauthorized
from ..models import BKUser,Login_status
from . import api
from flask import g,jsonify
from .. import db

auth = HTTPBasicAuth()

# # @api.before_request
# @auth.login_required
# def before_request():
#     pass
#     # if not g.current_user.is_anonymous() and \
#     #         not g.current_user.confirmed:
#     #     return forbidden('Unconfirmed account')

@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')

#使用用户手机号+密码/手机号+短信验证码/token 三种验证方法
@auth.verify_password
def verify_password(phonenumber_or_token,password_or_confirm_num):
    # 验证token
    user = BKUser.verify_auth_token(phonenumber_or_token).first()
    print(phonenumber_or_token)
    if not user:
        print(u'token验证不通过')
        # 尝试手机号+密码验证
        user = BKUser.query.filter_by(user_phone = phonenumber_or_token).first()
        if not user:
            #用户不存在
            print(u"用户不存在")
            return False
        if not user.verify_password(password_or_confirm_num):
            print(u'密码验证不通过')
            return False
        if user.user_current_token !=password_or_confirm_num:
            print(u"短信验证不通过,存入g")
            return False
        #密码或者短信验证通过时若用户处于登出状态，则改为登陆状态
        g.current_user = user
        if g.current_user.user_login_status==Login_status.LOGOUT:
            g.current_user.user_login_status=Login_status.LOGIN
            db.session.add(g.current_user)
            db.session.commit()
        return True
    #token验证通过，此时若用户处于登陆状态，就可使用token验证
    if user.user_login_status == Login_status.LOGIN:
        return True
    #否则不可使用token验证，只能同过另外两种方式
    else:
        return False

@api.route('/get_token')
@auth.login_required
def get_auth_token():
    token = g.current_user.generate_auth_token(0)
    return jsonify({ 'token': token.decode('ascii') })