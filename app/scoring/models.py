from app import db


# Robot score behavior and calculation
class RobotScore(db.Model):
    __tablename__ = 'robot_scores'

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    round_number = db.Column(db.Integer)

    # 2014 prototype data, remove once all 2015 data in place
    tree_branch_is_closer = db.Column(db.Boolean)
    tree_branch_is_intact = db.Column(db.Boolean)
    cargo_plane_location = db.Column(db.Integer)

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
                 tree_branch_is_closer=False,
                 tree_branch_is_intact=False,
                 cargo_plane_location=0):
        self.team_id = team
        self.round_number = round_number
        self.tree_branch_is_closer = tree_branch_is_closer
        self.tree_branch_is_intact = tree_branch_is_intact
        self.cargo_plane_location = cargo_plane_location

    def getScore(self):
        score = 0
        if self.tree_branch_is_closer and self.tree_branch_is_intact:
            score += 30
        score += self.get_plane_score(self.cargo_plane_location)
        return score

    def get_plane_score(self, argument):
        switcher = {
            0: 0,
            1: 20,
            2: 30,
            }
        return switcher.get(argument, 0)
