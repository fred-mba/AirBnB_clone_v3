#!/usr/bin/python3
"""Retrive State objects"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, State


@app_views.route('/states', methods=["GET"], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=["GET"], strict_slashes=False)
def states(state_id=None):
    """Retrives lists of all state objects if no state id is given,
       else if valid, a single state object response."""

    if state_id:
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        return jsonify(state.to_dict())

    else:
        states = [state_obj.to_dict()
                  for state_obj in storage.all(State).values()]
        print(type(states))
        return jsonify(states)


@app_views.route('/states/<state_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_state(state_id=None):
    """"Deletes a state object"""
    if state_id:
        state = storage.get(State, state_id)
        if not state:
            abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=["POST"], strict_slashes=False)
def create_state(state_id=None):
    """Creates a state"""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    if 'name' not in data:
        abort(400, description="Missing name")

    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=["PUT"], strict_slashes=False)
def update_state(state_id=None):
    """"Updates the State object with all key-value pairs of the
    dictionary."""

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)

    state.save()
    return jsonify(state.to_dict())
