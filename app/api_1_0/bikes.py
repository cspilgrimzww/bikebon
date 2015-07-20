#coding=utf-8
__author__ = 'cspilgrim'
from ..models import BKBike,Status
from . import api
from flask import jsonify

@api.route('/bikes')
def get_bikes_list():
    bikes = BKBike.query.filter_by(BKBike.bike_status == Status.AVAILABLE).all()
    json_bikes = []
    for item in bikes:
        json_bike = item.to_json()
        json_bikes.append(json_bike)
    return jsonify({'bikes':json_bikes})

@api.route('/bikes/<id>')
def get_bike(id):
    bike = BKBike.query.get_or_404(id)
    return jsonify(bike.to_json())