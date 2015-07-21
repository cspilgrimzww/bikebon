#coding=utf-8
__author__ = 'cspilgrim'
from flask.ext.httpauth import HTTPBasicAuth
from .errors import forbidden, unauthorized
from ..models import BKUser,AnonymousUser
from . import api
from flask import g,jsonify

auth = HTTPBasicAuth()

# @api.before_request
@auth.login_required
def before_request():
    pass
    # if not g.current_user.is_anonymous() and \
    #         not g.current_user.confirmed:
    #     return forbidden('Unconfirmed account')

@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')

#使用用户手机号和token两种验证方法
@auth.verify_password
def verify_password(phonenumber_or_token,password):
    # first try to authenticate by token
    user = BKUser.verify_auth_token(phonenumber_or_token)
    if not user:
        print(u'token验证不通过')
        # try to authenticate with phone_number/password
        user = BKUser.query.filter_by(user_phone = phonenumber_or_token).first()
        if not user or not user.user_current_token !=password:
            print(u'用户不存在或密码验证不通过')
            return False
    g.current_user = user
    return True

@api.route('/get_token')
@auth.login_required
def get_auth_token():
    token = g.current_user.generate_auth_token(0)
    return jsonify({ 'token': token.decode('ascii') })