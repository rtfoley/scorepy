from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Robot score behavior and calculation
class RobotScore(db.Model):
    __tablename__ = 'robot_scores'

    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.Integer)
    tree_branch_is_closer = db.Column(db.Boolean)
    tree_branch_is_intact = db.Column(db.Boolean)
    cargo_plane_location = db.Column(db.Integer)

    def __init__(self, team=0, tree_branch_is_closer = False, tree_branch_is_intact = False, cargo_plane_location = 0):
        self.team = team
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
