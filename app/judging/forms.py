from flask.ext.wtf import Form
from wtforms import SelectField, RadioField
from .models import Presentation, Technical, CoreValues


class PresentationForm(Form):
    team_id = SelectField(u'Team', coerce=int)
    # Research
    problem_identification = RadioField(u'Problem identification',
                                        choices=[(i, i) for i in range(0, 5)],
                                        coerce=int,
                                        default=0)
    sources_of_information = RadioField(u'Sources of information',
                                        choices=[(i, i) for i in range(0, 5)],
                                        coerce=int,
                                        default=0)
    problem_analysis = RadioField(u'Problem analysis',
                                  choices=[(i, i) for i in range(0, 5)],
                                  coerce=int,
                                  default=0)
    existing_solutions = RadioField(u'Existing solutions',
                                    choices=[(i, i) for i in range(0, 5)],
                                    coerce=int,
                                    default=0)
    # Innovative Solution
    team_solution = RadioField(u'Team solution',
                               choices=[(i, i) for i in range(0, 5)],
                               coerce=int,
                               default=0)
    innovation = RadioField(u'Innovation',
                            choices=[(i, i) for i in range(0, 5)],
                            coerce=int,
                            default=0)
    implementation = RadioField(u'Implementation',
                                choices=[(i, i) for i in range(0, 5)],
                                coerce=int,
                                default=0)
    # Presentation
    sharing = RadioField(u'Sharing',
                         choices=[(i, i) for i in range(0, 5)],
                         coerce=int,
                         default=0)
    creativity = RadioField(u'Creativity',
                            choices=[(i, i) for i in range(0, 5)],
                            coerce=int,
                            default=0)
    effectiveness = RadioField(u'Effectiveness',
                               choices=[(i, i) for i in range(0, 5)],
                               coerce=int,
                               default=0)

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

        return True


class CoreValuesForm(Form):
    team_id = SelectField(u'Team', coerce=int)
    # Inspiration
    discovery = RadioField(u'Discovery',
                           choices=[(i, i) for i in range(0, 5)],
                           coerce=int,
                           default=0)
    team_spirit = RadioField(u'Team Spirit',
                             choices=[(i, i) for i in range(0, 5)],
                             coerce=int,
                             default=0)
    integration = RadioField(u'Inspiration',
                             choices=[(i, i) for i in range(0, 5)],
                             coerce=int,
                             default=0)
    # Teamwork
    effectiveness = RadioField(u'Effectiveness',
                               choices=[(i, i) for i in range(0, 5)],
                               coerce=int,
                               default=0)
    efficiency = RadioField(u'Efficiency',
                            choices=[(i, i) for i in range(0, 5)],
                            coerce=int,
                            default=0)
    kids_do_the_work = RadioField(u'Kids do the work',
                                  choices=[(i, i) for i in range(0, 5)],
                                  coerce=int,
                                  default=0)
    # Gracious Professionalism
    inclusion = RadioField(u'Inclusion',
                           choices=[(i, i) for i in range(0, 5)],
                           coerce=int,
                           default=0)
    respect = RadioField(u'Respect',
                         choices=[(i, i) for i in range(0, 5)],
                         coerce=int,
                         default=0)
    coopertition = RadioField(u'Coopertition',
                              choices=[(i, i) for i in range(0, 5)],
                              coerce=int,
                              default=0)

    def validate(self):
        # Base validation
        rv = Form.validate(self)
        if not rv:
            return False

        # Team-ID fields doesn't exist on an 'edit' form
        if not self.team_id:
            return True

        # New score being entered, check if one already exists for team/ round
        t = CoreValues.query.filter_by(team_id=self.team_id.data).first()
        if t is not None:
            self.team_id.errors.append("Entry already exists for this team")
            return False

        return True


class TechnicalForm(Form):
    team_id = SelectField(u'Team', coerce=int)
    # Mechanical Design
    mechanical_durability = RadioField(u'Mechanical durability',
                                       choices=[(i, i) for i in range(0, 5)],
                                       coerce=int,
                                       default=0)
    mechanical_efficiency = RadioField(u'Mechanical efficiency',
                                       choices=[(i, i) for i in range(0, 5)],
                                       coerce=int,
                                       default=0)
    mechanization = RadioField(u'Mechanization',
                               choices=[(i, i) for i in range(0, 5)],
                               coerce=int,
                               default=0)
    # Programming
    programming_quality = RadioField(u'Programming quality',
                                     choices=[(i, i) for i in range(0, 5)],
                                     coerce=int,
                                     default=0)
    programming_efficiency = RadioField(u'Programming efficiency',
                                        choices=[(i, i) for i in range(0, 5)],
                                        coerce=int,
                                        default=0)
    autonomous_navigation = RadioField(u'Autonomous navigation',
                                       choices=[(i, i) for i in range(0, 5)],
                                       coerce=int,
                                       default=0)
    # Strategy and Innovation
    design_process = RadioField(u'Design process',
                                choices=[(i, i) for i in range(0, 5)],
                                coerce=int,
                                default=0)
    mission_strategy = RadioField(u'Mission strategy',
                                  choices=[(i, i) for i in range(0, 5)],
                                  coerce=int,
                                  default=0)
    innovation = RadioField(u'Innovation',
                            choices=[(i, i) for i in range(0, 5)],
                            coerce=int,
                            default=0)

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

        return True
