from flask.ext.wtf import Form
from wtforms import SelectField, BooleanField, IntegerField, TextField, \
    validators, SubmitField
from models import RobotScore


class TeamForm(Form):
    number = IntegerField("Number", [validators.Required(),
                                     validators.NumberRange(min=1, max=99999)])
    name = TextField("Name", [validators.Required(),
                              validators.Length(min=1, max=50)])
    affiliation = TextField("Affiliation", [validators.Length(min=1, max=200)])
    city = TextField("City", [validators.Length(min=1, max=50)])
    state = TextField("State", [validators.Length(min=2, max=2)])
    submit = SubmitField(u'Submit')


class ScoreForm(Form):
    team_id = SelectField(u'Team', coerce=int)
    round_number = SelectField(u'Round',
                               choices=[(1, '1'), (2, '2'), (3, '3')],
                               coerce=int)
    tree_branch_is_closer = BooleanField(u'Is tree branch closer to mat than \
                                         power lines', default=False)
    tree_branch_is_intact = BooleanField(u'Is tree branch model intact',
                                         default=False)
    cargo_plane_location = SelectField(u'Cargo plane location',
                                       choices=[('0', 'None'),
                                                ('1', 'Yellow only'),
                                                ('2', 'Light blue')])
    submit = SubmitField(u'Submit')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.score = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        score = RobotScore.query.filter_by(round_number=self.round_number.data,
                                           team_id=self.team_id.data).first()
        if score is not None:
            self.round_number.errors.append("Score already exists for this \
                                            round")
            return False

        self.score = score
        return True
