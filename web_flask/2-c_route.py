from flask import flask
""" start flask application
routes:
 /: Displays 'Hello HBNB!'.
    /hbnb: Displays 'HBNB'.
    /c/<text>: Displays 'C' followed by the value of <text>.
"""
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    formatted_text = text.replace('_', '')
    return "C {}".format(formatted_text)

if __name__ == '__main__':
    app.run(host='0.0.0.0", port=5000)
