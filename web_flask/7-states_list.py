#!/usr/bin/python3
"""List all State objects in DBstorage"""

from flask import Flask, render_template, g
from models import storage, DBStorage
from models.state import State


app = Flask(__name__)


def get_db():
    if "db" not in g:
        g.db = storage._DBStorage__session
    return g.db


@app.route('/states_list', strict_slashes=False)
def states_list():
    """List of all State objects present in DBStorage sorted by name (A->Z)"""
    if hasattr(storage, "_DBStorage__session"):
        db = get_db()
        result = db.query(State).order_by(State.name).all()
    return render_template('7-states_list.html', list_state=result)


@app.teardown_appcontext
def teardown_appctx(exception):
    """Ensures DB session is removed after each request"""
    db = g.pop("db", None)
    if db is not None:
        storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
