from flask.ext.wtf import Form
from wtforms import SelectField, RadioField
from .models import Presentation, Technical, Teamwork, TeamSpirit


class PresentationForm(Form):
    team_id = SelectField(u'Team', coerce=int)
    problem_identification = RadioField(u'Problem identification',
                                        choices=[(i, i) for i in range(0, 5)],
                                        coerce=int)
    sources_of_information = RadioField(u'Sources of information',
                                        choices=[(i, i) for i in range(0, 5)],
                                        coerce=int)
    problem_analysis = RadioField(u'Problem analysis',
                                  choices=[(i, i) for i in range(0, 5)],
                                  coerce=int)
    existing_solutions = RadioField(u'Existing solutions',
                                    choices=[(i, i) for i in range(0, 5)],
                                    coerce=int)
    team_solution = RadioField(u'Team solution',
                               choices=[(i, i) for i in range(0, 5)],
                               coerce=int)
    innovation = RadioField(u'Innovation',
                            choices=[(i, i) for i in range(0, 5)],
                            coerce=int)
    implementation = RadioField(u'Implementation',
                                choices=[(i, i) for i in range(0, 5)],
                                coerce=int)
    sharing = RadioField(u'Sharing',
                         choices=[(i, i) for i in range(0, 5)],
                         coerce=int)
    creativity = RadioField(u'Creativity',
                            choices=[(i, i) for i in range(0, 5)],
                            coerce=int)
    effectiveness = RadioField(u'Effectiveness',
                               choices=[(i, i) for i in range(0, 5)],
                               coerce=int)
    inclusion = RadioField(u'Inclusion',
                           choices=[(i, i) for i in range(0, 5)],
                           coerce=int)
    respect = RadioField(u'Respect',
                         choices=[(i, i) for i in range(0, 5)],
                         coerce=int)

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
    effectiveness = RadioField(u'Effectiveness',
                               choices=[(i, i) for i in range(0, 5)],
                               coerce=int)
    efficiency = RadioField(u'Efficiency',
                            choices=[(i, i) for i in range(0, 5)],
                            coerce=int)
    kids_do_the_work = RadioField(u'Kids do the work',
                                  choices=[(i, i) for i in range(0, 5)],
                                  coerce=int)
    inclusion = RadioField(u'Inclusion',
                           choices=[(i, i) for i in range(0, 5)],
                           coerce=int)
    respect = RadioField(u'Respect',
                         choices=[(i, i) for i in range(0, 5)],
                         coerce=int)

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
    mechanical_durability = RadioField(u'Mechanical durability',
                                       choices=[(i, i) for i in range(0, 5)],
                                       coerce=int)
    mechanical_efficiency = RadioField(u'Mechanical efficiency',
                                       choices=[(i, i) for i in range(0, 5)],
                                       coerce=int)
    mechanization = RadioField(u'Mechanization',
                               choices=[(i, i) for i in range(0, 5)],
                               coerce=int)
    programming_quality = RadioField(u'Programming quality',
                                     choices=[(i, i) for i in range(0, 5)],
                                     coerce=int)
    programming_efficiency = RadioField(u'Programming efficiency',
                                        choices=[(i, i) for i in range(0, 5)],
                                        coerce=int)
    autonomous_navigation = RadioField(u'Autonomous navigation',
                                       choices=[(i, i) for i in range(0, 5)],
                                       coerce=int)
    design_process = RadioField(u'Design process',
                                choices=[(i, i) for i in range(0, 5)],
                                coerce=int)
    mission_strategy = RadioField(u'Mission strategy',
                                  choices=[(i, i) for i in range(0, 5)],
                                  coerce=int)
    innovation = RadioField(u'Innovation',
                            choices=[(i, i) for i in range(0, 5)],
                            coerce=int)

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
    inspiration = RadioField(u'Inspiration',
                             choices=[(i, i) for i in range(0, 5)],
                             coerce=int)

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
