#!/usr/bin/python3
"""View module for Amenity objects"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, Amenity


@app_views.route('/amenities', methods=["GET"], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=["GET"],
                 strict_slashes=False)
def amenities(amenity_id=None):
    """
    Retrive:
    - List of all amenities objects(/amenities)
    - Single amenity objects by their ids(/amenities/<amenity_id>).
    """

    if amenity_id:
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)

        return jsonify(amenity.to_dict())
    else:
        amenities = [amenity.to_dict()
                     for amenity in storage.all(Amenity).values()]
        return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id=None):
    """"Deletes a amenity object given its id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=["POST"], strict_slashes=False)
def create_amenity():
    """Creates a amenity object"""
    data = request.get_json(force=True)
    if not data:
        abort(400, description="Not a JSON")

    if 'name' not in data:
        abort(400, description="Missing name")

    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id=None):
    """"
    Updates amenity object.
    Ignores: id, created_at and updated_at.
    """

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    data = request.get_json(force=True)
    if not data:
        abort(400, description="Not a JSON")

    ignore = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore:
            setattr(amenity, key, value)

    amenity.save()
    return jsonify(amenity.to_dict())
