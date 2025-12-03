#!/usr/bin/python3
"""Place view module that handles all RESTful API actions"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, Place, City, User


@app_views.route('/cities/<city_id>/places', methods=["GET"],
                 strict_slashes=False)
@app_views.route('/places/<place_id>', methods=["GET"], strict_slashes=False)
def city_places(place_id=None, city_id=None):
    """
    Retrive:
      - List of all Place objects of a City: (/cities/<city_id>/places)
      - A single place using place id (places/<place_id>)
    """

    if city_id:
        city = storage.get(City, city_id)

        if not city:
            abort(404)
        places = [place.to_dict() for place in city.places]
        return jsonify(places)

    if place_id:
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_place(place_id=None):
    """"Deletes place object given its id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=["POST"],
                 strict_slashes=False)
def create_place(city_id=None):
    """Creates a place linked to the given city id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    # (silent=True)Avoid automatic 415 error
    data = request.get_json(silent=True)

    if data is None or not request.is_json:
        abort(400, description="Not a JSON")

    if 'user_id' not in data:
        abort(400, description="Missing user_id")

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    if 'name' not in data:
        abort(400, description="Missing name")

    new_place = Place(**data)
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=["PUT"], strict_slashes=False)
def update_place(place_id=None):
    """
    Updates place object.
    Ignores: id, user_id, city_id, created_at, and updated_at.
    """

    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    data = request.get_json(silent=True)

    if data is None or not request.is_json:
        abort(400, description="Not a JSON")

    ignore = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict())
