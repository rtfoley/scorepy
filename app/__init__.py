# Python library imports
from flask import Flask
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

# setup application
app = Flask(__name__)
app.config.from_object('config')
Bootstrap(app)

db = SQLAlchemy(app)
db.init_app(app)

from app.awards.models import AwardCategory

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
    return render_template("pit_display.html")


# Pit Display page
@app.route("/settings", methods=['GET'])
def settings():
    categories = AwardCategory.query.all()
    return render_template("settings.html", categories=sorted(categories, key=by_name))


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# Sort awards by name
def by_name(award):
    return award.name


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
