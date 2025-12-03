#!/usr/bin/python3
"""City view module that handles all RESTful API actions"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, State, City


@app_views.route('/cities/<city_id>', methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """Get single city object by its id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route('/states/<state_id>/cities', methods=["GET"],
                 strict_slashes=False)
def cities(state_id):
    """Retrives list of all city objects of a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """"Deletes a city object by its id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a city linked to the given state id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json(silent=True)

    if data is None or not request.is_json:
        abort(400, description="Not a JSON")

    if 'name' not in data:
        abort(400, description="Missing name")

    new_city = City(**data)
    new_city.state_id = state_id
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """"
    Updates city object.
    Ignores: id, state_id, created_at and updated_at.
    """

    city = storage.get(City, city_id)
    if not city:
        abort(404)

    data = request.get_json(silent=True)
    if data is None or not request.is_json:
        abort(400, description="Not a JSON")

    ignore = ["id", "state_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore:
            setattr(city, key, value)

    city.save()
    return jsonify(city.to_dict())
