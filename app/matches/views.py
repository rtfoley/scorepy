import csv
import os
from flask import Blueprint, flash, render_template, request, redirect, \
    url_for
from flask.ext.login import login_required
from app import db
from app.util import create_pdf
from models import Match, MatchSlot, CompetitionTable
from forms import UploadForm
from app.teams.models import Team


mod_matches = Blueprint('matches', __name__, url_prefix='/matches')


# Match list
@mod_matches.route("/")
def index():
    matches = Match.query.all()
    competition_tables = CompetitionTable.query.all()
    return render_template("matches/match_list.html", matches=matches, competition_tables=competition_tables)
    
@mod_matches.route("/upload", methods=['GET', 'POST'])
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
        # TODO wipe all previous tables/ matches, with warning first
        tables = addTablesFromCsv(filename)
        matchCount = addMatchesFromCsv(filename, tables)
        flash('Imported %d matches' % matchCount, 'success')

        os.remove(filename)
        return redirect(url_for(".index"))
    return render_template("matches/match_upload_form.html", form=form)

def addTablesFromCsv(filename):
    competition_tables = []

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)

        i = 0
        fields = reader.fieldnames
        table_names = filter(lambda k: 'Table' in k, fields)
        for table in table_names:
            comp_table = CompetitionTable(i, table)
            competition_tables.append(comp_table)
            db.session.add(comp_table)
            i += 1

        db.session.commit()
        return competition_tables

def addMatchesFromCsv(filename, tables):
    matches = []
    competition_tables = {}
    teams = {}

    for team in Team.query.all():
        teams[team.number] = team.id

    for table in tables:
        competition_tables[table.name] = table.id

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)

        j = 1
        for row in reader:
            # TODO handle 12pm correctly
            match = Match(j, 'Q', row['Round'], row['Time'])
            j += 1
            for key, value in competition_tables.iteritems():
                if row[key]:
                    team_id = Team.query.filter_by(number = row[key]).first().id
                    table_id = value
                    match.slots.append(MatchSlot(table_id, team_id))

            db.session.add(match)

        db.session.commit()

        return len(matches)



