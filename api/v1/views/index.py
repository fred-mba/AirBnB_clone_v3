#!/usr/bin/python3
"""Index route of the API"""

from flask import jsonify
from api.v1.views import app_views
from models import storage, dummy_tables


@app_views.route('/status', methods=['GET'])
def status():
    """Returns status of the API"""
    return jsonify({"status": "OK"}), 200


@app_views.route('/stats', methods=['GET'])
def stats():
    counts = {}

    for key, cls_name in dummy_tables.items():
        counts[key] = storage.count(cls_name)

    return jsonify(counts)
