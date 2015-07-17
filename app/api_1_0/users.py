# coding=utf8
__author__ = 'cspilgrim'
from ..models import BKUser,BKBike
from flask import jsonify
from . import api

@api.route('/users/<id>')
def get_user(id):
    # user = BKUser.query.get_or_404(id)
    user = BKUser(user_name=u"钟蔚蔚")
    return jsonify(user.to_json())
