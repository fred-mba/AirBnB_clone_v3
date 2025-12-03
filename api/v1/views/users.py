#!/usr/bin/python3
"""State view module to handle REST API actions"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, User


@app_views.route('/users', methods=["GET"], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=["GET"], strict_slashes=False)
def users(user_id=None):
    """
    Retrives:
    - Lists of all users(/users).
    - A single user by its id(/users/<user_id>)
    """

    if user_id:
        user = storage.get(User, user_id)
        if not user:
            abort(404)
        return jsonify(user.to_dict())

    else:
        users = [user_obj.to_dict()
                 for user_obj in storage.all(User).values()]
        return jsonify(users)


@app_views.route('/users/<user_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_user(user_id=None):
    """"Deletes a user by id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=["POST"], strict_slashes=False)
def create_user():
    """Creates a user"""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    if 'email' not in data:
        abort(400, description="Missing email")

    if 'password' not in data:
        abort(400, description="Missing password")

    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=["PUT"], strict_slashes=False)
def update_user(user_id=None):
    """"
    Updates the User object with all key-value pairs of the
    dictionary.
    """

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore = ["id", "email", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)

    user.save()
    return jsonify(user.to_dict())
