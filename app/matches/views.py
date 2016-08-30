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

        
        # wipe all previous tables/ matches, with warning first
        for existing_slot in MatchSlot.query.all():
            db.session.delete(existing_slot)
        
        for existing_table in CompetitionTable.query.all():
            db.session.delete(existing_table)
        
        for existing_match in Match.query.all():
            db.session.delete(existing_match)
            
        db.session.commit()
        
        # extract data from file
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
        
        # Get the fields that start with 'Table' (may want to make this more flexible later on)
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

    # setup team and table dictionaries for quick access
    for team in Team.query.all():
        teams[team.number] = team.id

    for table in tables:
        competition_tables[table.name] = table.id

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)

        j = 1
        for row in reader:
            # Create the overall match object
            match = Match(j, 'Q', row['Round'], row['Time'])
            
            j += 1
            for key, value in competition_tables.iteritems():
                # if there is a team number in the table column, then add a match-slot object
                if row[key]:
                    team_id = Team.query.filter_by(number = row[key]).first().id
                    table_id = value
                    match.slots.append(MatchSlot(table_id, team_id))

            matches.append(match)
            db.session.add(match)

        db.session.commit()

        return len(matches)


