from app import db
from app.scoring.models import RobotScore
from app.judging.models import Presentation, Technical, CoreValues
from app.awards.models import AwardWinner
from operator import attrgetter


class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(50))
    affiliation = db.Column(db.String(200))
    city = db.Column(db.String(50))
    state = db.Column(db.String(2))
    is_rookie = db.Column(db.Boolean)
    highest_round_reached = db.Column(db.Integer)
    scores = db.relationship('RobotScore', backref='team')
    presentation = db.relationship('Presentation', uselist=False,
                                   backref='team')
    technical = db.relationship('Technical', uselist=False, backref='team')
    core_values = db.relationship('CoreValues', uselist=False, backref='team')
    awards = db.relationship('AwardWinner', backref='team')

    def __init(self, number, name, affiliation, city, state, is_rookie):
        self.number = number
        self.name = name
        self.affiliation = affiliation
        self.city = city
        self.state = state
        self.is_rookie = is_rookie
        self.highest_round_reached = 0

    def get_score_for_round(self, round_number):
        return next((score for score in self.scores if
                     score.round_number == round_number), None)

    @property
    def round1(self):
        return self.get_score_for_round(1)

    @property
    def round2(self):
        return self.get_score_for_round(2)

    @property
    def round3(self):
        return self.get_score_for_round(3)

    @property
    def best(self):
        if self.scores:
            return max(self.scores, key=attrgetter('total'))
        else:
            return None
