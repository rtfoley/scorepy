from flask.ext.wtf import Form
from wtforms import SelectField, RadioField, IntegerField
from models import RobotScore


class ScoreForm(Form):
    team_id = SelectField(u'Team', coerce=int)
    round_number = SelectField(u'Round',
                               choices=[(1, '1'), (2, '2'), (3, '3')],
                               coerce=int)
    # M04 yellow/ blue bars
    bars_in_west_transfer = IntegerField('Yellow/ Blue Bars in matching green bins completely on/in West Transfer',
                                         default=0)
    bars_never_in_west_transfer = IntegerField(
        'Yellow/ Blue Bars in matching green bins NEVER completely on/in West Transfer ', default=0)

    # M04 black bars
    black_bars_in_original_position = IntegerField('Black Bars in original position / scoring Flower Box', default=12)
    black_bars_in_green_or_landfill = IntegerField('Black bars in matching Green Bin or Landfill', default=0)
    black_bars_elsewhere = IntegerField('Black bars elsewhere in play', default=0)

    # M02 Methane
    methane_in_truck_or_factory = RadioField(u'Methane in Truck and/or Factory',
                                             choices=[(0, '0'),
                                                      (1, '1'),
                                                      (2, '2')],
                                             coerce=int,
                                             default=0)

    # M03 Transport
    truck_supports_yellow_bin = RadioField(u'Truck supports all of Yellow Bin\'s weight',
                                           choices=[('False', 'No'), ('True', 'Yes')],
                                           default='False')
    yellow_bin_east_of_guide = RadioField(u'Yellow Bin completely East of Truck\'s guide',
                                          choices=[('False', 'No'), ('True', 'Yes')],
                                          default='False')

    # M05 Careers
    anyone_in_sorter_area = RadioField(u'1+ people completely in Sorter Area',
                                       choices=[('False', 'No'), ('True', 'Yes')],
                                       default='False')

    # M06 Scrap Cars
    engine_installed = RadioField(u'Engine/ Windshield installed in unfolded car',
                                  choices=[('False', 'No'), ('True', 'Yes')],
                                  default='False')
    car_folded_in_east_transfer = RadioField(u'Car completely folded in East Transfer',
                                             choices=[('False', 'No'), ('True', 'Yes')],
                                             default='False')
    car_never_in_safety = RadioField(u'Car never even partly in Safety',
                                     choices=[('False', 'No'), ('True', 'Yes')],
                                     default='False')

    # M08 Composting
    compost_ejected_not_in_safety = RadioField(u'Compost ejected, NOT completely in Safety',
                                               choices=[('False', 'No'), ('True', 'Yes')],
                                               default='False')
    compost_ejected_in_safety = RadioField(u'Compost ejected, AND completely in Safety',
                                           choices=[('False', 'No'), ('True', 'Yes')],
                                           default='False')

    # M07 Cleanup
    plastic_bags_in_safety = RadioField(u'Plastic Bags completely in Safety',
                                        choices=[(0, '0'),
                                                 (1, '1'),
                                                 (2, '2')],
                                        coerce=int,
                                        default=0)
    animals_in_circles_without_bags = RadioField(u'Animals completely in any Circle without Bags',
                                                 choices=[(0, '0'),
                                                          (1, '1'),
                                                          (2, '2'),
                                                          (3, '3')],
                                                 coerce=int,
                                                 default=0)
    chicken_in_small_landfill_circle = RadioField(u'Chicken completely in Small Landfill Circle',
                                                  choices=[('False', 'No'), ('True', 'Yes')],
                                                  default='False')

    # M10 Demolition
    all_beams_not_in_setup_position = RadioField(u'All Beams no longer in setup position',
                                                 choices=[('False', 'No'), ('True', 'Yes')],
                                                 default='False')

    # M01 Recycled Material
    green_bins_in_opp_safety = RadioField(u'Your Green Bins w/ Matching Yellow/ Blue bars in Opposing Safety',
                                          choices=[(0, '0'),
                                                   (1, '1'),
                                                   (2, '2')],
                                          coerce=int,
                                          default=0)
    opp_green_bins_in_safety = RadioField(u'Opposing Green Bins w/ Matching Yellow/ Blue bars in Your Safety',
                                          choices=[(0, '0'),
                                                   (1, '1'),
                                                   (2, '2')],
                                          coerce=int,
                                          default=0)

    # M09 Salvage
    valuables_in_safety = RadioField(u'Valuables completely in Safety',
                                     choices=[('False', 'No'), ('True', 'Yes')],
                                     default='False')

    # M11 Purchasing Decisions
    planes_in_safety = RadioField(u'Toy Planes completely in Safety',
                                  choices=[(0, '0'),
                                           (1, '1'),
                                           (2, '2')],
                                  coerce=int,
                                  default=0)

    # M12 Repurposing
    compost_in_toy_package = RadioField(u'Compost perfectly nested in empty Toy Package',
                                        choices=[('False', 'No'), ('True', 'Yes')],
                                        default='False')
    package_in_original_condition = RadioField(u'Package in original condition',
                                               choices=[('False', 'No'), ('True', 'Yes')],
                                               default='False')

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
