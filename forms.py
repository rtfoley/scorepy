from flask.ext.wtf import Form
from wtforms import SelectField, BooleanField, IntegerField, TextField, \
    validators


class TeamForm(Form):
    number = IntegerField("Number", [validators.Required(),
                                     validators.NumberRange(min=1, max=99999)])
    name = TextField("Name", [validators.Required(),
                              validators.Length(min=1, max=50)])
    affiliation = TextField("Affiliation", [validators.Length(min=1, max=200)])
    city = TextField("City", [validators.Length(min=1, max=50)])
    state = TextField("State", [validators.Length(min=2, max=2)])


# TODO add validation
class ScoreForm(Form):
    team_id = SelectField(u'Team', coerce=int)
    round_number = SelectField(u'Round', choices=[(1, '1'), (2, '2'), (3, '3')], coerce=int)
    tree_branch_is_closer = BooleanField(default=False)
    tree_branch_is_intact = BooleanField(default=False)
    cargo_plane_location = SelectField(choices=[('0', 'None'),
                                                ('1', 'Yellow only'),
                                                ('2', 'Light blue')])
