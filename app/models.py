from sqlalchemy.ext.hybrid import hybrid_property
from flask.ext.login import UserMixin
from app import bcrypt, db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True)
    _password = db.Column(db.String(128))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def is_correct_password(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext)
        
class EventSettings(db.Model):
    __tablename__ = 'event_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    is_championship = db.Column(db.Boolean)
    quarter_finals_teams = db.Column(db.Integer)
    semi_finals_teams = db.Column(db.Integer)
    finals_teams = db.Column(db.Integer)
    
    def __init__(self, name, championship, quarter_finals_teams = 8, semi_finals_teams=4, finals_teams = 2):
        self.name = name
        self.is_championship = championship
        self.quarter_finals_teams = quarter_finals_teams
        self.semi_finals_teams = semi_finals_teams
        self.finals_teams = finals_teams