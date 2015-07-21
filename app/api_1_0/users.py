# coding=utf8
__author__ = 'cspilgrim'
from .. import db
from ..models import BKUser
from flask import jsonify, request
from . import api
from .help_utils import generate_confirm_number
from .help_utils import request_confirm_number
from .authentication import auth
from ..models import Status

# 获取用户个人信息
@api.route('/users/<int:id>')
@auth.login_required
def get_user(id):
    user = BKUser.query.get_or_404(id)
    return jsonify(user.to_json())

# 获取短信验证码
@api.route('/users/get_comfirm_num',methods=['POST'])
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
        return jsonify({})
    return jsonify({"error":"confirm_error"})
