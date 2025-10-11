#!/usr/bin/python3
"""Create flask instance and run the API"""

from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_appctx(exception):
    """Close db connection after each request"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)
