import csv
import os
from flask import Blueprint, flash, render_template, request, redirect, \
    url_for
from flask.ext.login import login_required
from app import db
from app.util import create_pdf
from models import Team
from forms import TeamForm, UploadForm


# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_teams = Blueprint('teams', __name__, url_prefix='/teams')


# Team list
@mod_teams.route("/")
def index():
    teams = Team.query.all()
    return render_template("teams/teams.html",
                           teams=sorted(teams, key=by_team))


# add a new team
@mod_teams.route("/new", methods=['GET', 'POST'])
@login_required
def add():
    form = TeamForm()
    if request.method == 'POST' and form.validate_on_submit():
        team = Team()
        form.populate_obj(team)
        db.session.add(team)
        db.session.commit()
        return redirect(url_for(".index"))
    elif request.method == 'POST':
        flash('Failed validation', 'danger alert-auto-dismiss')
    return render_template("teams/team_form.html", form=form, id=None)


# Upload teams via CSV file
@mod_teams.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if request.method == 'POST' and 'file' in request.files:
        # define filename for the uploaded file
        filename = 'uploaded_teams.csv'

        # delete any existing copies of the uploaded file
        if os.path.isfile(filename):
            os.remove(filename)
            print 'removed file'

        # get the file from the POST data
        file = request.files['file']
        file.save(filename)

        # extract team data from file
        teams = extractTeamsFromCsv(filename)

        # add teams to database
        teamCount = 0
        for team in teams:
            # make sure team doesn't already exist first
            existing = Team.query.filter_by(number=team.number).first()
            if existing is None:
                db.session.add(team)
                teamCount = teamCount + 1
        if teamCount > 0:
            db.session.commit()

        flash('Imported %d teams' % teamCount, 'success')
        os.remove(filename)
        return redirect(url_for(".index"))
    return render_template("teams/team_upload_form.html", form=form)


def extractTeamsFromCsv(filename):
    teams = []
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            team = Team(number=int(row['Number']),
                        name=row['Name'],
                        affiliation=row['Affiliation'],
                        city=row['City'],
                        state=row['State'],
                        is_rookie=row['Rookie'] == 'True')
            teams.append(team)
    return teams


# Edit a previously-entered team
@mod_teams.route("/<int:team_id>/edit", methods=['GET', 'POST'])
@login_required
def edit(team_id):
    team = Team.query.get(team_id)
    form = TeamForm(obj=team)
    del form.number

    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(team)
        db.session.commit()
        return redirect(url_for(".index"))
    elif request.method == 'POST':
        flash('Failed validation', 'danger alert-auto-dismiss')
    return render_template("teams/team_form.html", form=form, number=team.number, id=team.id)


# Delete a team
@mod_teams.route("/<int:team_id>/delete", methods=['GET', 'POST'])
@login_required
def delete(team_id):
    team = Team.query.get(team_id)
    if request.method == 'POST':
        # delete related scores
        for score in team.scores:
            db.session.delete(score)

        # delete related judging entries
        if team.presentation is not None:
            db.session.delete(team.presentation)
        if team.technical is not None:
            db.session.delete(team.technical)
        if team.core_values is not None:
            db.session.delete(team.core_values)

        # clear any assigned awards
        for award in team.awards:
            award.team_id = None

        # delete the team
        db.session.delete(team)
        db.session.commit()
        return redirect(url_for(".index"))
    return render_template("delete.html", identifier="team %d" % team.number)


# Team PDF report
@mod_teams.route('/teams_report.pdf')
def teams_pdf():
    teams = Team.query.all()
    team_report = render_template("teams/team_report.html",
                                  teams=sorted(teams, key=by_team))
    pdf = create_pdf(team_report, 'teams.pdf')
    return pdf


@mod_teams.route("/category_results.pdf", methods=['GET'])
@login_required
def category_results_pdf():
    teams = Team.query.all()
    data = render_template("teams/category_results.html",
                           teams=sorted(teams, key=by_team))

    pdf = create_pdf(data, 'category_results.pdf')
    return pdf


# Sort teams by number
def by_team(team):
    return team.number
