from flask.ext.wtf import Form
from wtforms import SelectField, BooleanField, IntegerField, TextField, \
    validators, SubmitField
from models import RobotScore, Presentation, Technical, Teamwork, TeamSpirit


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


class TeamworkForm(Form):
    team_id = SelectField(u'Team', coerce=int)
    effectiveness = SelectField(u'Effectiveness',
                                choices=[(i, i) for i in range(0, 5)],
                                coerce=int)
    efficiency = SelectField(u'Efficiency',
                             choices=[(i, i) for i in range(0, 5)],
                             coerce=int)
    kids_do_the_work = SelectField(u'Kids do the work',
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
        t = Teamwork.query.filter_by(team_id=self.team_id.data).first()
        if t is not None:
            self.team_id.errors.append("Entry already exists for this team")
            return False

        self.t = t
        return True


class TechnicalForm(Form):
    team_id = SelectField(u'Team', coerce=int)
    mechanical_durability = SelectField(u'Mechanical durability',
                                        choices=[(i, i) for i in range(0, 5)],
                                        coerce=int)
    mechanical_efficiency = SelectField(u'Mechanical efficiency',
                                        choices=[(i, i) for i in range(0, 5)],
                                        coerce=int)
    mechanization = SelectField(u'Mechanization',
                                choices=[(i, i) for i in range(0, 5)],
                                coerce=int)
    programming_quality = SelectField(u'Programming quality',
                                      choices=[(i, i) for i in range(0, 5)],
                                      coerce=int)
    programming_efficiency = SelectField(u'Programming efficiency',
                                         choices=[(i, i) for i in range(0, 5)],
                                         coerce=int)
    autonomous_navigation = SelectField(u'Autonomous navigation',
                                        choices=[(i, i) for i in range(0, 5)],
                                        coerce=int)
    design_process = SelectField(u'Design process',
                                 choices=[(i, i) for i in range(0, 5)],
                                 coerce=int)
    mission_strategy = SelectField(u'Mission strategy',
                                   choices=[(i, i) for i in range(0, 5)],
                                   coerce=int)
    innovation = SelectField(u'Innovation',
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
        t = Technical.query.filter_by(team_id=self.team_id.data).first()
        if t is not None:
            self.team_id.errors.append("Entry already exists for this team")
            return False

        self.t = t
        return True


class TeamSpiritForm(Form):
    team_id = SelectField(u'Team', coerce=int)
    inspiration = SelectField(u'Inspiration',
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
        t = TeamSpirit.query.filter_by(team_id=self.team_id.data).first()
        if t is not None:
            self.team_id.errors.append("Entry already exists for this team")
            return False

        self.t = t
        return True
