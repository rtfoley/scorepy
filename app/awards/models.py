from enum import Enum
from app import db


class AwardCategory(Enum):
    Champions = 0
    Research = 1
    Presentation = 2
    Innovative_Solution = 3
    Mechanical_Design = 4
    Programming = 5
    Strategy_and_Innovation = 6
    Teamwork = 7
    Inspiration = 8
    Gracious_Professionalism = 9
    Robot_Performance = 10

    @property
    def friendly_name(self):
        return self._name_.replace("_", " ") + " Award"


class AwardWinner(db.Model):
    __tablename__ = 'award_winners'

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=True)
    category_id = db.Column(db.Integer)
    place = db.Column(db.Integer)

    def __init__(self, team_id=None, category_id=0, place=0):
        self.team_id = team_id
        self.category_id = category_id
        self.place = place

    @property
    def friendly_award_name(self):
        if self.place == 0:
            place_text = "1st"
        elif self.place == 1:
            place_text = "2nd"
        else:
            place_text = "3rd"

        return "%s, %s place" % (AwardCategory(self.category_id).friendly_name, place_text)
