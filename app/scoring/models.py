from app import db


# Robot score behavior and calculation
class RobotScore(db.Model):
    __tablename__ = 'robot_scores'

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    round_number = db.Column(db.Integer)

    # M04 yellow/ blue bars
    bars_in_west_transfer = db.Column(db.Integer)
    bars_never_in_west_transfer = db.Column(db.Integer)

    # M04 black bars
    black_bars_in_original_position = db.Column(db.Integer)
    black_bars_in_green_or_landfill = db.Column(db.Integer)
    black_bars_elsewhere = db.Column(db.Integer)

    # M02 Methane
    methane_in_truck_or_factory = db.Column(db.Integer)

    # M03 Transport
    truck_supports_yellow_bin = db.Column(db.Boolean)
    yellow_bin_east_of_guide = db.Column(db.Boolean)

    # M05 Careers
    anyone_in_sorter_area = db.Column(db.Boolean)

    # M06 Scrap Cars
    engine_installed = db.Column(db.Boolean)
    car_folded_in_east_transfer = db.Column(db.Boolean)
    car_never_in_safety = db.Column(db.Boolean)

    # M08 Composting
    compost_ejected_not_in_safety = db.Column(db.Boolean)
    compost_ejected_in_safety = db.Column(db.Boolean)

    # M07 Cleanup
    plastic_bags_in_safety = db.Column(db.Integer)
    animals_in_circles_without_bags = db.Column(db.Integer)
    chicken_in_small_landfill_circle = db.Column(db.Boolean)

    # M10 Demolition
    all_beams_not_in_setup_position = db.Column(db.Boolean)

    # M01 Recycled Material
    green_bins_in_opp_safety = db.Column(db.Integer)
    opp_green_bins_in_safety = db.Column(db.Integer)

    # M09 Salvage
    valuables_in_safety = db.Column(db.Boolean)

    # M11 Purchasing Decisions
    planes_in_safety = db.Column(db.Integer)

    # M12 Repurposing
    compost_in_toy_package = db.Column(db.Boolean)
    package_in_original_condition = db.Column(db.Boolean)

    def __init__(self,
                 team=0,
                 round_number=1,
                 # M04 yellow/ blue bars
                 bars_in_west_transfer=0,
                 bars_never_in_west_transfer=0,

                 # M04 black bars
                 black_bars_in_original_position=12,
                 black_bars_in_green_or_landfill=0,
                 black_bars_elsewhere=0,

                 # M02 Methane
                 methane_in_truck_or_factory=0,

                 # M03 Transport
                 truck_supports_yellow_bin=False,
                 yellow_bin_east_of_guide=False,

                 # M05 Careers
                 anyone_in_sorter_area=False,

                 # M06 Scrap Cars
                 engine_installed=False,
                 car_folded_in_east_transfer=False,
                 car_never_in_safety=False,

                 # M08 Composting
                 compost_ejected_not_in_safety=False,
                 compost_ejected_in_safety=False,

                 # M07 Cleanup
                 plastic_bags_in_safety=0,
                 animals_in_circles_without_bags=0,
                 chicken_in_small_landfill_circle=False,

                 # M10 Demolition
                 all_beams_not_in_setup_position=False,

                 # M01 Recycled Material
                 green_bins_in_opp_safety=0,
                 opp_green_bins_in_safety=0,

                 # M09 Salvage
                 valuables_in_safety=False,

                 # M11 Purchasing Decisions
                 planes_in_safety=0,

                 # M12 Repurposing
                 compost_in_toy_package=False,
                 package_in_original_condition=False):
        self.team_id = team
        self.round_number = round_number

        # M04 yellow/ blue bars
        self.bars_in_west_transfer = bars_in_west_transfer
        self.bars_never_in_west_transfer = bars_never_in_west_transfer

        # M04 black bars
        self.black_bars_in_original_position = black_bars_in_original_position
        self.black_bars_in_green_or_landfill = black_bars_in_green_or_landfill
        self.black_bars_elsewhere = black_bars_elsewhere

        # M02 Methane
        self.methane_in_truck_or_factory = methane_in_truck_or_factory

        # M03 Transport
        self.truck_supports_yellow_bin = truck_supports_yellow_bin
        self.yellow_bin_east_of_guide = yellow_bin_east_of_guide

        # M05 Careers
        self.anyone_in_sorter_area = anyone_in_sorter_area

        # M06 Scrap Cars
        self.engine_installed = engine_installed
        self.car_folded_in_east_transfer = car_folded_in_east_transfer
        self.car_never_in_safety = car_never_in_safety

        # M08 Composting
        self.compost_ejected_not_in_safety = compost_ejected_not_in_safety
        self.compost_ejected_in_safety = compost_ejected_in_safety

        # M07 Cleanup
        self.plastic_bags_in_safety = plastic_bags_in_safety
        self.animals_in_circles_without_bags = animals_in_circles_without_bags
        self.chicken_in_small_landfill_circle = chicken_in_small_landfill_circle

        # M10 Demolition
        self.all_beams_not_in_setup_position = all_beams_not_in_setup_position

        # M01 Recycled Material
        self.green_bins_in_opp_safety = green_bins_in_opp_safety
        self.opp_green_bins_in_safety = opp_green_bins_in_safety

        # M09 Salvage
        self.valuables_in_safety = valuables_in_safety

        # M11 Purchasing Decisions
        self.planes_in_safety = planes_in_safety

        # M12 Repurposing
        self.compost_in_toy_package = compost_in_toy_package
        self.package_in_original_condition = package_in_original_condition

    def getScore(self):
        score = 0
        return score

    def get_plane_score(self, argument):
        switcher = {
            0: 0,
            1: 20,
            2: 30,
        }
        return switcher.get(argument, 0)
