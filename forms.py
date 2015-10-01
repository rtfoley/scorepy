from flask.ext.wtf import Form
from wtforms import SelectField, BooleanField, IntegerField, TextField

class TeamForm(Form):
    number = IntegerField()
    name = TextField()
    affiliation = TextField()
    city = TextField()
    state = TextField()

class ScoreForm(Form):
    team = SelectField(u'Team')
    tree_branch_is_closer = BooleanField(default=False)
    tree_branch_is_intact = BooleanField(default=False)
    cargo_plane_location = SelectField(choices=[('0', 'None'), ('1', 'Yellow only'), ('2', 'Light blue')])
