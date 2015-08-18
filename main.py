# Python library imports
import flask
from flask import render_template, request, jsonify

# Imports from other parts of the app
from forms import ScoreForm
from models import RobotScore

# setup application
app = flask.Flask(__name__)
app.config.from_object('config')

# Maine route
@app.route("/")
def index():
    form = ScoreForm()
    return render_template("index.html", form=form)

# Utility method to get live score when score form is being filled out
@app.route('/_add_numbers')
def add_numbers():
    score = RobotScore(treebranchcloser = request.args.get('treebranchcloser')=='true', treebranchintact = request.args.get('treebranchintact')=='true', cargoplane = request.args.get('cargoplane', 0, type=int))
    return jsonify(result=score.getScore())

if __name__ == "__main__":
    app.run(debug = True)
