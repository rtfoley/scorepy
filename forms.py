from flask.ext.wtf import Form
from wtforms import SelectField, BooleanField, IntegerField, TextField, \
    validators, SubmitField
from models import RobotScore, Presentation


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
        # Base validation
        rv = Form.validate(self)
        if not rv:
            return False

        # Team-ID and round-number fields don't exist on an 'edit' form
        if not self.team_id or not self.round_number:
            return True

        # New score being entered, check if one already exists for team/ round
        score = RobotScore.query.filter_by(round_number=self.round_number.data,
                                           team_id=self.team_id.data).first()
        if score is not None:
            self.round_number.errors.append("Score already exists for this \
                                            round")
            return False

        self.score = score
        return True


class PresentationForm(Form):
    team_id = SelectField(u'Team', coerce=int)
    problem_identification = SelectField(u'Problem identification',
                                         choices=[(i, i) for i in range(0, 5)],
                                         coerce=int)
    sources_of_information = SelectField(u'Sources of information',
                                         choices=[(i, i) for i in range(0, 5)],
                                         coerce=int)
    problem_analysis = SelectField(u'Problem analysis',
                                   choices=[(i, i) for i in range(0, 5)],
                                   coerce=int)
    existing_solutions = SelectField(u'Existing solutions',
                                     choices=[(i, i) for i in range(0, 5)],
                                     coerce=int)
    team_solution = SelectField(u'Team solution',
                                choices=[(i, i) for i in range(0, 5)],
                                coerce=int)
    innovation = SelectField(u'Innovation',
                             choices=[(i, i) for i in range(0, 5)],
                             coerce=int)
    implementation = SelectField(u'Implementation',
                                 choices=[(i, i) for i in range(0, 5)],
                                 coerce=int)
    sharing = SelectField(u'Sharing',
                          choices=[(i, i) for i in range(0, 5)],
                          coerce=int)
    creativity = SelectField(u'Creativity',
                             choices=[(i, i) for i in range(0, 5)],
                             coerce=int)
    effectiveness = SelectField(u'Effectiveness',
                                choices=[(i, i) for i in range(0, 5)],
                                coerce=int)
    inclusion = SelectField(u'Inclusion',
                            choices=[(i, i) for i in range(0, 5)],
                            coerce=int)
    respect = SelectField(u'Respect',
                          choices=[(i, i) for i in range(0, 5)],
                          coerce=int)
    submit = SubmitField(u'Submit')

    def validate(self):
        # Base validation
        rv = Form.validate(self)
        if not rv:
            return False

        # Team-ID fields doesn't exist on an 'edit' form
        if not self.team_id:
            return True

        # New score being entered, check if one already exists for team/ round
        p = Presentation.query.filter_by(team_id=self.team_id.data).first()
        if p is not None:
            self.team_id.errors.append("Entry already exists for this team")
            return False

        self.p = p
        return True

