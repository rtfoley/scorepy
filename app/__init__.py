# Python library imports
from flask import Flask
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy

# setup application
app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


# Playoffs page
@app.route("/playoffs", methods=['GET'])
def playoffs():
    return render_template("playoffs.html")


# Pit Display page
@app.route("/pit", methods=['GET'])
def pit_display():
    return render_template("pit_display.html", title="Southern Maine FLL Qualifier", subtitle="Rankings")


# Pit Display page
@app.route("/settings", methods=['GET'])
def settings():
    return render_template("settings.html")


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# Import a module / component using its blueprint handler variable (mod_auth)
from app.teams.views import mod_teams as teams_module
from app.scoring.views import mod_scoring as scoring_module
from app.judging.views import mod_judging as judging_module
from app.awards.views import mod_awards as awards_module

# Register blueprint(s)
app.register_blueprint(teams_module)
app.register_blueprint(scoring_module)
app.register_blueprint(judging_module)
app.register_blueprint(awards_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
