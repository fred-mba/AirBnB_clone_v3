#!/usr/bin/python3
"""Places review view module that handles all RESTful API actions"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, Place, Review, User


@app_views.route('/places/<place_id>/reviews', methods=["GET"],
                 strict_slashes=False)
@app_views.route('/reviews/<review_id>', methods=["GET"], strict_slashes=False)
def reviews(place_id=None, review_id=None):
    """Retrives:
    - List of all reviews of a place(/places/<place_id>/reviews)
    - A single review object by its id(/reviews/<review_id>)
    """
    if place_id:
        place = storage.get(Place, place_id)
        if not place:
            abort(404)

        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)

    if review_id:
        review = storage.get(Review, review_id)
        if not review:
            abort(404)

        return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_review(review_id=None):
    """"Deletes a review object by its id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=["POST"],
                 strict_slashes=False)
def create_place_review(place_id=None):
    """Creates a place review by place id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    data = request.get_json(silent=True)
    if data is None or not request.is_json:
        abort(400, description="Not a JSON")

    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    if 'text' not in data:
        abort(400, description="Missing text")

    new_review = Review(**data)
    new_review.place_id = place_id
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=["PUT"], strict_slashes=False)
def update_place_review(review_id=None):
    """"
    Updates review object.
    Ignores: id, user_id, place_id, created_at and updated_at.
    """

    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    data = request.get_json(silent=True)

    if data is None or not request.is_json:
        abort(400, description="Not a JSON")

    ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore:
            setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict())
