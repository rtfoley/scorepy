from app import db


class AwardCategory(db.Model):
    __tablename__ = 'award_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    winner = db.relationship('AwardWinner', backref='category')


class AwardWinner(db.Model):
    __tablename__ = 'award_winners'

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('award_categories.id'))
    place = db.Column(db.Integer)
