from app import db


class AwardWinner(db.Model):
    __tablename__ = 'award_winners'

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    category_id = db.Column(db.Integer)
    place = db.Column(db.Integer)