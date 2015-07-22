# coding=utf8
__author__ = 'cspilgrim'
from .. import db
from ..models import BKUser
from flask import jsonify, request,g
from . import api
from .help_utils import generate_confirm_number
from .help_utils import request_confirm_number
from .authentication import auth
from ..models import Status

# 获取用户个人信息
@api.route('/users/user')
@auth.login_required
def get_user():
    id = g.current_user.user_id
    user = BKUser.query.get_or_404(id)
    return jsonify(user.to_json())

# 获取短信验证码
@api.route('/users/get_confirm_num',methods=['POST'])
def get_confirm_num():
    phone_num = str(request.json.get('phone_number'))
    confirm_num = generate_confirm_number()
    user = BKUser()
    user.user_current_token = confirm_num
    user.user_phone = phone_num
    db.session.add(user)
    db.session.commit()
    answer = request_confirm_number(phone_num,confirm_num)
    return jsonify(answer)

# 验证短信验证码
@api.route('/users/confirm_user',methods=['POST'])
def confirm_user():
    received_num = str(request.json.get('confirm_number'))
    received_phone_number = str(request.json.get('phone_number'))
    user = BKUser.query.filter_by(user_phone = received_phone_number).first()
    if str(user.user_current_token) == received_num:
        print('两码一致')

        user.user_confirmed = True
        db.session.add(user)
        db.session.commit()
        token = user.generate_auth_token(3600*24*365*100)
        return jsonify({ 'token': token.decode('ascii') })
    return jsonify({"error":"confirm_error"})

# 提交用户的验证信息到数据库

@api.route('/users/verify_user',methods=['POST'])
@auth.login_required
def add_user_verify_info():
    g.current_user.user_name=request.json.get('user_name')
    g.current_user.user_identity_number=request.json.get('user_identity_number')
    g.current_user.user_student_identity_number=request.json.get('user_student_identity_number')
    db.session.add(g.current_user)
    db.session.commit()
    return jsonify({})

