__author__ = 'cspilgrim'
from flask.ext.httpauth import HTTPBasicAuth
from .errors import forbidden, unauthorized
from ..models import BKUser,AnonymousUser
from . import api
from flask import g,jsonify

auth = HTTPBasicAuth()

@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and \
            not g.current_user.confirmed:
        return forbidden('Unconfirmed account')

@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')

@auth.verify_password
def verify_password(token,password):
    if token == '':
        g.current_user = AnonymousUser()
        return True
    if password == '':
        g.current_user = BKUser.verify_auth_token(token)
        g.token_used =True
        return g.current_user is not None
    user = BKUser.query.filter_by()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return  BKUser.verify_auth_token(password)

@api.route('/token')
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token':g.current_user.generate_auth_token(
        expiration = 3600),'expiration':3600})