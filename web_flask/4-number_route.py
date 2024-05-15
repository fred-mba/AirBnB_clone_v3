from flask import flask
""" start flask application
routes:
 /: Displays 'Hello HBNB!'.
    /hbnb: Displays 'HBNB'.
    /c/<text>: Displays 'C' followed by the value of <text>.
    /python/<text>: display “Python ”, followed by the value of the text
"""
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    formatted_text = text.replace('_', ' ')
    return 'C {}'.format(formatted_text)


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=false)
def python_text(test='is cool'):
    formatted_text = text.replace('_', ' ')
    return 'python {}'.format(formatted_text)


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    return "{:d} is a number".forman(n)

if __name__ == '__main__':
    app.run(host='0.0.0.0", port=5000)
