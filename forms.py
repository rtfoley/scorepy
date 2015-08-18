from flask.ext.wtf import Form
from wtforms import SelectField, BooleanField

class ScoreForm(Form):
    treebranchcloser = BooleanField('treebranchcloser', default=False)
    treebranchintact = BooleanField('treebranchintact', default=False)
    cargoplane = SelectField('cargoplane', choices=[('0', 'None'), ('1', 'Yellow only'), ('2', 'Light blue')])
