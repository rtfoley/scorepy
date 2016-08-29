from flask.ext.wtf import Form
from wtforms import SelectField, SelectField, IntegerField
from models import RobotScore
from app.teams.models import Team


class ScoreForm(Form):
    team_id = SelectField(u'Team', coerce=int)
    round_number = SelectField(u'Round', coerce=int)
    # M04 yellow/ blue bars
    bars_in_west_transfer = SelectField('4. Yellow/ Blue Bars in matching green bins completely on/in West Transfer',
                                        choices=[(x, '%d' % x) for x in range(0, 16)],
                                        coerce=int,
                                        default=0)
    bars_never_in_west_transfer = SelectField(
        '4. Yellow/ Blue Bars in matching green bins NEVER completely on/in West Transfer ',
        choices=[(x, '%d' % x) for x in range(0, 16)],
        coerce=int,
        default=0)

    # M04 black bars
    black_bars_in_original_position = SelectField('4. Black Bars in original position / scoring Flower Box',
                                                  choices=[(x, '%d' % x) for x in range(0, 13)],
                                                  coerce=int,
                                                  default=12)
    black_bars_in_green_or_landfill = SelectField('4. Black bars in matching Green Bin or Landfill',
                                                  choices=[(x, '%d' % x) for x in range(0, 9)],
                                                  coerce=int,
                                                  default=0)
    black_bars_elsewhere = SelectField('4. Black bars elsewhere in play',
                                       choices=[(x, '%d' % x) for x in range(0, 13)],
                                       coerce=int,
                                       default=0)

    # M02 Methane
    methane_in_truck_or_factory = SelectField('2. Methane in Truck and/or Factory',
                                              choices=[(0, '0'),
                                                       (1, '1'),
                                                       (2, '2')],
                                              coerce=int,
                                              default=0)

    # M03 Transport
    # TODO this could be switched to a boolean coersion if radio field not going to be used
    truck_supports_yellow_bin = SelectField('3. Truck supports all of Yellow Bin\'s weight',
                                            choices=[('False', '0 - No'), ('True', '1 - Yes')],
                                            default='False')
    # TODO this could be switched to a boolean coersion if radio field not going to be used
    yellow_bin_east_of_guide = SelectField('3. Yellow Bin completely East of Truck\'s guide',
                                           choices=[('False', '0 - No'), ('True', '1 - Yes')],
                                           default='False')

    # M05 Careers
    # TODO this could be switched to a boolean coersion if radio field not going to be used
    anyone_in_sorter_area = SelectField('5. 1+ people completely in Sorter Area',
                                        choices=[('False', '0 - No'), ('True', '1 - Yes')],
                                        default='False')

    # M06 Scrap Cars
    # TODO this could be switched to a boolean coersion if radio field not going to be used
    engine_installed = SelectField('6. Engine/ Windshield installed in unfolded car',
                                   choices=[('False', '0 - No'), ('True', '1 - Yes')],
                                   default='False')
    # TODO this could be switched to a boolean coersion if radio field not going to be used
    car_folded_in_east_transfer = SelectField('6. Car completely folded in East Transfer',
                                              choices=[('False', '0 - No'), ('True', '1 - Yes')],
                                              default='False')
    # TODO this could be switched to a boolean coersion if radio field not going to be used
    car_never_in_safety = SelectField('6. Car never even partly in Safety',
                                      choices=[('False', '0 - No'), ('True', '1 - Yes')],
                                      default='False')

    # M08 Composting
    # TODO this could be switched to a boolean coersion if radio field not going to be used
    compost_ejected_not_in_safety = SelectField('8. Compost ejected, NOT completely in Safety',
                                                choices=[('False', '0 - No'), ('True', '1 - Yes')],
                                                default='False')
    # TODO this could be switched to a boolean coersion if radio field not going to be used
    compost_ejected_in_safety = SelectField('8. Compost ejected, AND completely in Safety',
                                            choices=[('False', '0 - No'), ('True', '1 - Yes')],
                                            default='False')

    # M07 Cleanup
    plastic_bags_in_safety = SelectField('7. Plastic Bags completely in Safety',
                                         choices=[(0, '0'),
                                                  (1, '1'),
                                                  (2, '2')],
                                         coerce=int,
                                         default=0)
    animals_in_circles_without_bags = SelectField('7. Animals completely in any Circle without Bags',
                                                  choices=[(0, '0'),
                                                           (1, '1'),
                                                           (2, '2'),
                                                           (3, '3')],
                                                  coerce=int,
                                                  default=0)
    # TODO this could be switched to a boolean coersion if radio field not going to be used
    chicken_in_small_landfill_circle = SelectField('7. Chicken completely in Small Landfill Circle',
                                                   choices=[('False', '0 - No'), ('True', '1 - Yes')],
                                                   default='False')

    # M10 Demolition
    # TODO this could be switched to a boolean coersion if radio field not going to be used
    all_beams_not_in_setup_position = SelectField('10. All Beams no longer in setup position',
                                                  choices=[('False', '0 - No'), ('True', '1 - Yes')],
                                                  default='False')

    # M01 Recycled Material
    green_bins_in_opp_safety = SelectField('1. Your Green Bins w/ Matching Yellow/ Blue bars in Opposing Safety',
                                           choices=[(0, '0'),
                                                    (1, '1'),
                                                    (2, '2')],
                                           coerce=int,
                                           default=0)
    opp_green_bins_in_safety = SelectField('1. Opposing Green Bins w/ Matching Yellow/ Blue bars in Your Safety',
                                           choices=[(0, '0'),
                                                    (1, '1'),
                                                    (2, '2')],
                                           coerce=int,
                                           default=0)

    # M09 Salvage
    # TODO this could be switched to a boolean coersion if radio field not going to be used
    valuables_in_safety = SelectField('9. Valuables completely in Safety',
                                      choices=[('False', '0 - No'), ('True', '1 - Yes')],
                                      default='False')

    # M11 Purchasing Decisions
    planes_in_safety = SelectField('11. Toy Planes completely in Safety',
                                   choices=[(0, '0'),
                                            (1, '1'),
                                            (2, '2')],
                                   coerce=int,
                                   default=0)

    # M12 Repurposing
    # TODO this could be switched to a boolean coersion if radio field not going to be used
    compost_in_toy_package = SelectField('12. Compost perfectly nested in empty Toy Package',
                                         choices=[('False', '0 - No'), ('True', '1 - Yes')],
                                         default='False')
    # TODO this could be switched to a boolean coersion if radio field not going to be used
    package_in_original_condition = SelectField('12. Package in original condition',
                                                choices=[('False', '0 - No'), ('True', '1 - Yes')],
                                                default='False')

    def validate(self):
        # Base validation
        rv = Form.validate(self)
        if not rv:
            return False

        form_valid = True

        # Team-ID and round-number fields don't exist on an 'edit' form
        if self.team_id and self.round_number:
            if self.team_id.data==-1:
                self.team_id.errors.append("Please select a team")
                form_valid = False

            if self.round_number.data==-1:
                self.round_number.errors.append("Please select a round")
                form_valid = False

            if self.team_id.data != -1 and self.round_number.data != -1:
                # New score being entered, check if one already exists for team/ round
                score = RobotScore.query.filter_by(round_number=self.round_number.data,
                                                   team_id=self.team_id.data).first()
                if score is not None:
                    self.round_number.errors.append("Score already exists for this \
                                                round")
                    form_valid = False
                else:
                    # Ensure that the selected round is valid for this team
                    team = Team.query.filter_by(id=self.team_id.data).one()
                    if self.round_number.data >= 4 and team.highest_round_reached < self.round_number.data:
                        self.round_number.errors.append(
                            "Team is not participating in the selected round, please select another")
                        form_valid = False

        # Check that compost isn't marked as being both in and out of safety
        if self.compost_ejected_in_safety.data == 'True' and self.compost_ejected_not_in_safety.data == 'True':
            self.compost_ejected_not_in_safety.errors.append("Compost cannot be both in and not in safety")
            self.compost_ejected_in_safety.errors.append("Compost cannot be both in and not in safety")
            form_valid = False

        # Check that car isn't marked as folded and engine installed (not physically possible)
        if self.car_folded_in_east_transfer.data == 'True' and self.engine_installed.data == 'True':
            self.car_folded_in_east_transfer.errors.append("Engine can't be installed when car is folded")
            self.engine_installed.errors.append("Engine can't be installed when car is folded")
            form_valid = False

        # Check that total number of black bars equals 12
        total_black_bars = self.black_bars_in_original_position.data \
                           + self.black_bars_in_green_or_landfill.data \
                           + self.black_bars_elsewhere.data

        if total_black_bars != 12:
            self.black_bars_in_original_position.errors.append("Total number of black bars must equal 12")
            self.black_bars_in_green_or_landfill.errors.append("Total number of black bars must equal 12")
            self.black_bars_elsewhere.errors.append("Total number of black bars must equal 12")
            form_valid = False

        return form_valid
