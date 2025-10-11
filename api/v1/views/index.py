#!/usr/bin/python3
"""Index route of the API"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """Returns status of the API"""
    return jsonify({"status": "OK"}), 200
