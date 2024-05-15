from flask import flask
""" start flask application
routes:
 /: Displays 'Hello HBNB!'.
    /hbnb: Displays 'HBNB'.
"""
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return "HBNB"

if __name__ == '__main__':
    app.run(host='0.0.0.0", port=5000)
