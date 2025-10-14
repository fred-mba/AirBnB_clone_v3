#!/usr/bin/python3
"""Index route of the API"""

from flask import jsonify
from api.v1.views import app_views
from models import storage, Amenity, City, Place, Review, State, User


@app_views.route('/status', methods=['GET'])
def status():
    """Returns status of the API"""
    return jsonify({"status": "OK"}), 200


@app_views.route('/stats', methods=['GET'])
def stats():
    return jsonify({
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    })
