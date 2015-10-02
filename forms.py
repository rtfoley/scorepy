from flask.ext.wtf import Form
from wtforms import SelectField, BooleanField, IntegerField, TextField

# TODO add vailidation
class TeamForm(Form):
    number = IntegerField()
    name = TextField()
    affiliation = TextField()
    city = TextField()
    state = TextField()

class ScoreForm(Form):
    team_id = SelectField(u'Team', coerce=int)
    tree_branch_is_closer = BooleanField(default=False)
    tree_branch_is_intact = BooleanField(default=False)
    cargo_plane_location = SelectField(choices=[('0', 'None'), ('1', 'Yellow only'), ('2', 'Light blue')])
