from flask.ext.wtf import Form
from wtforms import SelectField, RadioField
from .models import Presentation, Technical, CoreValues

# Default choices for judging fields
default_choices = [(0, '0 - ND'), (1, '1'), (2, '2'), (3, '3'), (4, '4')]


class PresentationForm(Form):
    team_id = SelectField(u'Team', coerce=int)
    # Research
    problem_identification = SelectField(u'Problem identification',
                                         choices=default_choices,
                                         coerce=int,
                                         default=0)
    sources_of_information = SelectField(u'Sources of information',
                                         choices=default_choices,
                                         coerce=int,
                                         default=0)
    problem_analysis = SelectField(u'Problem analysis',
                                   choices=default_choices,
                                   coerce=int,
                                   default=0)
    existing_solutions = SelectField(u'Existing solutions',
                                     choices=default_choices,
                                     coerce=int,
                                     default=0)
    # Innovative Solution
    team_solution = SelectField(u'Team solution',
                                choices=default_choices,
                                coerce=int,
                                default=0)
    innovation = SelectField(u'Innovation',
                             choices=default_choices,
                             coerce=int,
                             default=0)
    implementation = SelectField(u'Implementation',
                                 choices=default_choices,
                                 coerce=int,
                                 default=0)
    # Presentation
    sharing = SelectField(u'Sharing',
                          choices=default_choices,
                          coerce=int,
                          default=0)
    creativity = SelectField(u'Creativity',
                             choices=default_choices,
                             coerce=int,
                             default=0)
    effectiveness = SelectField(u'Effectiveness',
                                choices=default_choices,
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
    discovery = SelectField(u'Discovery',
                            choices=default_choices,
                            coerce=int,
                            default=0)
    team_spirit = SelectField(u'Team Spirit',
                              choices=default_choices,
                              coerce=int,
                              default=0)
    integration = SelectField(u'Inspiration',
                              choices=default_choices,
                              coerce=int,
                              default=0)
    # Teamwork
    effectiveness = SelectField(u'Effectiveness',
                                choices=default_choices,
                                coerce=int,
                                default=0)
    efficiency = SelectField(u'Efficiency',
                             choices=default_choices,
                             coerce=int,
                             default=0)
    kids_do_the_work = SelectField(u'Kids do the work',
                                   choices=default_choices,
                                   coerce=int,
                                   default=0)
    # Gracious Professionalism
    inclusion = SelectField(u'Inclusion',
                            choices=default_choices,
                            coerce=int,
                            default=0)
    respect = SelectField(u'Respect',
                          choices=default_choices,
                          coerce=int,
                          default=0)
    coopertition = SelectField(u'Coopertition',
                               choices=default_choices,
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
    mechanical_durability = SelectField(u'Mechanical durability',
                                        choices=default_choices,
                                        coerce=int,
                                        default=0)
    mechanical_efficiency = SelectField(u'Mechanical efficiency',
                                        choices=default_choices,
                                        coerce=int,
                                        default=0)
    mechanization = SelectField(u'Mechanization',
                                choices=default_choices,
                                coerce=int,
                                default=0)
    # Programming
    programming_quality = SelectField(u'Programming quality',
                                      choices=default_choices,
                                      coerce=int,
                                      default=0)
    programming_efficiency = SelectField(u'Programming efficiency',
                                         choices=default_choices,
                                         coerce=int,
                                         default=0)
    autonomous_navigation = SelectField(u'Autonomous navigation',
                                        choices=default_choices,
                                        coerce=int,
                                        default=0)
    # Strategy and Innovation
    design_process = SelectField(u'Design process',
                                 choices=default_choices,
                                 coerce=int,
                                 default=0)
    mission_strategy = SelectField(u'Mission strategy',
                                   choices=default_choices,
                                   coerce=int,
                                   default=0)
    innovation = SelectField(u'Innovation',
                             choices=default_choices,
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
