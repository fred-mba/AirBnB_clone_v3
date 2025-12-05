#!/usr/bin/python3
"""
View link module between Place objects and Amenity Objects that handles
all default RESTful API actions.
"""

from flask import jsonify, abort
from api.v1.views import app_views
from models import storage, Place, Amenity
import os


@app_views.route('/places/<place_id>/amenities', methods=["GET"],
                 strict_slashes=False)
def place_amenity(place_id):
    """Retrieve list of amenity objects linked to a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify([amenity.to_dict() for amenity in place.amenities])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """"Deletes amenity object of a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)

    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)

    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=["POST"],
                 strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """Link amenity object to a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200

        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200

        place.amenity_ids.append(amenity_id)

    storage.save()
    return jsonify(amenity.to_dict()), 201
