from flask.ext.wtf import Form
from wtforms import SelectField, SubmitField
from .models import Presentation, Technical, Teamwork, TeamSpirit


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

    # TODO this code is duplicated in each judging form class, combine?
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
