import flask
from flask import render_template, request, jsonify

app = flask.Flask(__name__)

@app.route('/_add_numbers')
def add_numbers():
    treebranchcloser = request.args.get('treebranchcloser', 0, type=int)
    treebranchintact = request.args.get('treebranchintact', 0, type=int)
    cargoplane = request.args.get('cargoplane', 0, type=int)

    score = 0
    score += 30 if treebranchcloser == 1 and treebranchintact == 1 else 0
    score += get_plane_score(cargoplane)

    return jsonify(result=score)

def get_plane_score(argument):
    switcher = {
        0: 0,
        1: 20,
        2: 30,
    }
    return switcher.get(argument, 0)

@app.route("/")
def hello():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)
