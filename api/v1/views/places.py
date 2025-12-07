#!/usr/bin/python3
"""Place view module that handles all RESTful API actions"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, Place, City, User, State


@app_views.route('/places/<place_id>', methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """Retrieve a single place using place id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/cities/<city_id>/places', methods=["GET"],
                 strict_slashes=False)
def city_places(city_id):
    """Retrive list of all place objects of a City"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """"Deletes place object given its id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
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
def update_place(place_id):
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


@app_views.route('/places_search', methods=["POST"], strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending on the JSON in
    the body of the request.
    - If the JSON body is empty or each list of all keys are empty:
      retrieve all Place objects.
    """
    data = request.get_json()

    if data is None or not request.is_json:
        abort(400, description="Not a JSON")

    # If JSON body is empty retrieve all Place objects
    if data == {}:
        return jsonify([obj_value.to_dict()
                       for obj_value in storage.all(Place).values()])

    city_list = []

    if 'states' in data:
        state_list = [storage.get(State, state_id)
                      for state_id in data['states']]
        for state in state_list:
            if state:
                city_list.extend(state.cities)

    if 'cities' in data:
        for city_id in data['cities']:
            city = storage.get(City, city_id)
            if city:
                city_list.append(city)

    place_list = [place.to_dict()
                  for city in city_list for place in city.places]
    return jsonify(place_list)
