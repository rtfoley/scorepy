from app import db
from app.teams.models import Team


class CompetitionTable(db.Model):
    __tablename__ = 'competition_tables'
    
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    name = db.Column(db.String(20))
    

class MatchSlot(db.Model):
    __tablename__ = 'match_slots'
    
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'))
    competition_table_id = db.Column(db.Integer, db.ForeignKey('competition_tables.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    

class Match(db.Model):
    __tablename__ = 'matches'
    
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    match_type = db.Column(db.String(1))
    round_number = db.Column(db.Integer)
    time = db.Column(db.DateTime)
    slots = db.relationship('MatchSlot', backref='match')
    
    
