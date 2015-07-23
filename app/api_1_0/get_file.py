__author__ = 'cspilgrim'
from authentication import auth
from flask import url_for,redirect
from . import api

@api.route("/file/home/heads/<int:id>")
def get_homepage_heads(id):
    if id == 1:
        return redirect(url_for('static', filename='homepage_head/head1.jpg', _external=True))
    elif id == 2:
        return redirect(url_for('static', filename='homepage_head/head2.jpg', _external=True))
    elif id == 3:
        return redirect(url_for('static', filename='homepage_head/head3.jpg', _external=True))
        # return redirect(url_for('static', filename='homepage_head/Hydrangeas.jpg', _external=True))
