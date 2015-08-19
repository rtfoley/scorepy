from flask.ext.wtf import Form
from wtforms import SelectField, BooleanField, IntegerField

class ScoreForm(Form):
    team = IntegerField()
    tree_branch_is_closer = BooleanField(default=False)
    tree_branch_is_intact = BooleanField(default=False)
    cargo_plane_location = SelectField(choices=[('0', 'None'), ('1', 'Yellow only'), ('2', 'Light blue')])
