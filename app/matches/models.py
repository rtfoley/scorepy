from app import db
from datetime import datetime


class CompetitionTable(db.Model):
    __tablename__ = 'competition_tables'
    
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    name = db.Column(db.String(20))
    slots = db.relationship('MatchSlot', backref='competition_table')

    def __init__(self, number, name):
        self.number = number
        self.name = name
    

class MatchSlot(db.Model):
    __tablename__ = 'match_slots'
    
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'))
    competition_table_id = db.Column(db.Integer, db.ForeignKey('competition_tables.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))

    def __init__(self, table_id, team_id):
        self.competition_table_id = table_id
        self.team_id = team_id


class Match(db.Model):
    __tablename__ = 'matches'
    
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    match_type = db.Column(db.String(1))
    round_number = db.Column(db.Integer)
    time = db.Column(db.DateTime)
    slots = db.relationship('MatchSlot', backref='match')

    def __init__(self, number, match_type, round_number, time):
        self.number = int(number)
        self.match_type = match_type
        self.time = datetime.strptime(time, '%I:%M')
        self.round_number = int(round_number)
