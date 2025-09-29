#!/usr/bin/python3
"""List all State objects in DBstorage"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """List of all State objects present in DBStorage sorted by name (A->Z)"""
    storage_dict = storage.all(State)
    #states_list = [val for val in storage_dict.values()]
    return render_template('7-states_list.html', lists_state=storage_dict)


@app.teardown_appcontext
def teardown_appctx(exception):
    """Ensures DB session is removed after each request"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
