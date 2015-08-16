import flask
from flask import render_template, request, jsonify
from flask.ext.wtf import Form
from wtforms import SelectField, BooleanField

app = flask.Flask(__name__)
app.config.from_object('config')

class ScoreForm(Form):
    treebranchcloser = BooleanField('treebranchcloser', default=False)
    treebranchintact = BooleanField('treebranchintact', default=False)
    cargoplane = SelectField('cargoplane', choices=[('0', 'None'), ('1', 'Yellow only'), ('2', 'Light blue')])

@app.route('/_add_numbers')
def add_numbers():
    treebranchcloser = request.args.get('treebranchcloser')
    treebranchintact = request.args.get('treebranchintact')
    cargoplane = request.args.get('cargoplane', 0, type=int)

    score = 0
    if treebranchcloser=='true' and treebranchintact=='true':
        print 'tree success'
        score += 30
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
    form = ScoreForm()
    return render_template("index.html", form=form)

if __name__ == "__main__":
    app.run(debug = True)
