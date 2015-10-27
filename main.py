# Python library imports
import flask
import csv
import os
from flask import flash, render_template, request, jsonify, redirect, url_for, \
    make_response
from flask_bootstrap import Bootstrap
from cStringIO import StringIO
from xhtml2pdf import pisa
from operator import attrgetter

# Imports from other parts of the app
from forms import ScoreForm, TeamForm, PresentationForm, TechnicalForm, \
    TeamworkForm, TeamSpiritForm, UploadForm
from models import RobotScore, Team, Presentation, Technical, Teamwork, \
    TeamSpirit, Award, db

# setup application
app = flask.Flask(__name__)
app.config.from_object('config')
Bootstrap(app)

db.init_app(app)


# Main route
@app.route("/")
def index():
    return render_template("index.html")


# Settings page
@app.route("/settings")
def settings():
    awards = Award.query.all()
    return render_template("settings.html", awards=sorted(awards, key=by_name))


# Team list
@app.route("/teams")
def team_list():
    teams = Team.query.all()
    return render_template("teams.html", teams=sorted(teams, key=by_team))


@app.route("/scores")
def score_list():
    teams = Team.query.all()
    for team in teams:
        sortTeamScores(team)
    return render_template("score_list.html", teams=sorted(teams, key=by_team))


@app.route("/judging")
def judging_list():
    teams = Team.query.all()
    return render_template("judging_list.html",
                           teams=sorted(teams, key=by_team))


# Add a new robot score
@app.route("/scores/new", methods=['GET', 'POST'])
def new_score():
    form = ScoreForm()
    form.team_id.choices = [(t.id, t.number) for t in
                            sorted(Team.query.all(), key=by_team)]

    if request.method == 'POST' and form.validate_on_submit():
        score = RobotScore()
        form.populate_obj(score)
        db.session.add(score)
        db.session.commit()
        return redirect(url_for("score_list"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("score_form.html", form=form)


# Edit a previously-entered score
@app.route("/scores/<int:score_id>/edit", methods=['GET', 'POST'])
def edit_score(score_id):
    score = RobotScore.query.get(score_id)
    form = ScoreForm(obj=score)
    del form.team_id
    del form.round_number

    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(score)
        db.session.commit()
        return redirect(url_for("score_list"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("score_form.html", form=form, team_id=score.team_id,
                           round_number=score.round_number)


# Delete a score
@app.route("/scores/<int:score_id>/delete", methods=['GET', 'POST'])
def delete_score(score_id):
    score = RobotScore.query.get(score_id)
    if request.method == 'POST':
        db.session.delete(score)
        db.session.commit()
        return redirect(url_for("score_list"))
    return render_template("delete.html", identifier="score for %d in round %d"
                           % (score.team.number, score.round_number))


# add a new team
@app.route("/teams/new", methods=['GET', 'POST'])
def new_team():
    form = TeamForm()
    if request.method == 'POST' and form.validate_on_submit():
        team = Team()
        form.populate_obj(team)
        db.session.add(team)
        db.session.commit()
        return redirect(url_for("team_list"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("team_form.html", form=form)


# Upload teams via CSV file
@app.route("/teams/upload", methods=['GET', 'POST'])
def upload_teams():
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

        flash('Imported %d teams' % teamCount)
        os.remove(filename)
        return redirect(url_for("team_list"))
    return render_template("team_upload_form.html", form=form)


def extractTeamsFromCsv(filename):
    teams = []
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            team = Team(number=int(row['Number']),
                        name=row['Name'],
                        affiliation=row['Affiliation'],
                        city=row['City'],
                        state=row['State'])
            teams.append(team)
    return teams


# Edit a previously-entered team
@app.route("/teams/<int:team_id>/edit", methods=['GET', 'POST'])
def edit_team(team_id):
    team = Team.query.get(team_id)
    form = TeamForm(obj=team)
    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(team)
        db.session.commit()
        return redirect(url_for("team_list"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("team_form.html", form=form)


# Delete a team
@app.route("/teams/<int:team_id>/delete", methods=['GET', 'POST'])
def delete_team(team_id):
    team = Team.query.get(team_id)
    if request.method == 'POST':
        # delete related scores
        for score in team.scores:
            db.session.delete(score)

        # delete the team
        db.session.delete(team)
        db.session.commit()
        return redirect(url_for("team_list"))
    return render_template("delete.html", identifier="team %d" % team.number)


# Add a presentation judging entry
@app.route('/judging/presentation/new', methods=['GET', 'POST'])
def add_presentation():
    form = PresentationForm()
    form.team_id.choices = [(t.id, t.number) for t in
                            sorted(Team.query.all(), key=by_team)]
    if request.method == 'POST' and form.validate_on_submit():
        presentation = Presentation()
        form.populate_obj(presentation)
        db.session.add(presentation)
        db.session.commit()
        return redirect(url_for("judging_list"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("basic_form.html", form=form,
                           title='Presentation Form')


# Edit a previously-entered presentation judging entry
@app.route("/judging/presentation/<int:presentation_id>/edit",
           methods=['GET', 'POST'])
def edit_presentation(presentation_id):
    presentation = Presentation.query.get(presentation_id)
    form = PresentationForm(obj=presentation)
    del form.team_id

    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(presentation)
        db.session.commit()
        return redirect(url_for("judging_list"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("basic_form.html", form=form,
                           team_id=presentation.team_id,
                           title="Presentation Form")


# Delete a presentation judging entry
@app.route("/judging/presentation/<int:presentation_id>/delete",
           methods=['GET', 'POST'])
def delete_presentation(presentation_id):
    presentation = Presentation.query.get(presentation_id)
    if request.method == 'POST':
        db.session.delete(presentation)
        db.session.commit()
        return redirect(url_for("judging_list"))
    return render_template("delete.html",
                           identifier="presentation evaluation for team %d"
                           % presentation.team.number)


# Add a technical judging entry
@app.route('/judging/technical/new', methods=['GET', 'POST'])
def add_technical():
    form = TechnicalForm()
    form.team_id.choices = [(t.id, t.number) for t in
                            sorted(Team.query.all(), key=by_team)]
    if request.method == 'POST' and form.validate_on_submit():
        technical = Technical()
        form.populate_obj(technical)
        db.session.add(technical)
        db.session.commit()
        return redirect(url_for("judging_list"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("basic_form.html", form=form,
                           title='Technical Form')


# Edit a previously-entered technical judging entry
@app.route("/judging/technical/<int:technical_id>/edit",
           methods=['GET', 'POST'])
def edit_technical(technical_id):
    technical = Technical.query.get(technical_id)
    form = TechnicalForm(obj=technical)
    del form.team_id

    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(technical)
        db.session.commit()
        return redirect(url_for("judging_list"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("basic_form.html", form=form,
                           team_id=technical.team_id, title="Technical Form")


# Delete a technical judging entry
@app.route("/judging/technical/<int:technical_id>/delete",
           methods=['GET', 'POST'])
def delete_technical(technical_id):
    technical = Technical.query.get(technical_id)
    if request.method == 'POST':
        db.session.delete(technical)
        db.session.commit()
        return redirect(url_for("judging_list"))
    return render_template("delete.html",
                           identifier="technical evaluation for team %d"
                           % technical.team.number)


# Add a teamwork judging entry
@app.route('/judging/teamwork/new', methods=['GET', 'POST'])
def add_teamwork():
    form = TeamworkForm()
    form.team_id.choices = [(t.id, t.number) for t in
                            sorted(Team.query.all(), key=by_team)]
    if request.method == 'POST' and form.validate_on_submit():
        teamwork = Teamwork()
        form.populate_obj(teamwork)
        db.session.add(teamwork)
        db.session.commit()
        return redirect(url_for("judging_list"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("basic_form.html", form=form, title='Teamwork Form')


# Edit a previously-entered teamwork judging entry
@app.route("/judging/teamwork/<int:teamwork_id>/edit", methods=['GET', 'POST'])
def edit_teamwork(teamwork_id):
    teamwork = Teamwork.query.get(teamwork_id)
    form = TeamworkForm(obj=teamwork)
    del form.team_id

    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(teamwork)
        db.session.commit()
        return redirect(url_for("judging_list"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("basic_form.html", form=form,
                           team_id=teamwork.team_id, title="Teamwork Form")


# Delete a teamwork judging entry
@app.route("/judging/teamwork/<int:teamwork_id>/delete",
           methods=['GET', 'POST'])
def delete_teamwork(teamwork_id):
    teamwork = Teamwork.query.get(teamwork_id)
    if request.method == 'POST':
        db.session.delete(teamwork)
        db.session.commit()
        return redirect(url_for("judging_list"))
    return render_template("delete.html",
                           identifier="teamwork evaluation for team %d"
                           % teamwork.team.number)


# Add a team spirit judging entry
@app.route('/judging/team_spirit/new', methods=['GET', 'POST'])
def add_team_spirit():
    form = TeamSpiritForm()
    form.team_id.choices = [(t.id, t.number) for t in
                            sorted(Team.query.all(), key=by_team)]
    if request.method == 'POST' and form.validate_on_submit():
        team_spirit = TeamSpirit()
        form.populate_obj(team_spirit)
        db.session.add(team_spirit)
        db.session.commit()
        return redirect(url_for("judging_list"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("basic_form.html", form=form,
                           title='Team Spirit Form')


# Edit a previously-entered team spirit judging entry
@app.route("/judging/team_spirit/<int:team_spirit_id>/edit",
           methods=['GET', 'POST'])
def edit_team_spirit(team_spirit_id):
    team_spirit = TeamSpirit.query.get(team_spirit_id)
    form = TeamSpiritForm(obj=team_spirit)
    del form.team_id

    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(team_spirit)
        db.session.commit()
        return redirect(url_for("judging_list"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("basic_form.html", form=form,
                           team_id=team_spirit.team_id,
                           title="Team Spirit Form")


# Delete a team spirit judging entry
@app.route("/judging/team_spirit/<int:team_spirit_id>/delete",
           methods=['GET', 'POST'])
def delete_team_spirit(team_spirit_id):
    team_spirit = TeamSpirit.query.get(team_spirit_id)
    if request.method == 'POST':
        db.session.delete(team_spirit)
        db.session.commit()
        return redirect(url_for("judging_list"))
    return render_template("delete.html",
                           identifier="team spirit evaluation for team %d"
                           % team_spirit.team.number)


# Awards page
@app.route("/awards", methods=['GET'])
def awards():
    return render_template("awards.html")


# Playoffs page
@app.route("/playoffs", methods=['GET'])
def playoffs():
    return render_template("playoffs.html")


# Pit Display page
@app.route("/pit", methods=['GET'])
def pit_display():
    return render_template("pit_display.html")


# Create a PDF file from data
def create_pdf(pdf_data):
    pdf = StringIO()
    pisa.CreatePDF(StringIO(pdf_data.encode('utf-8')), pdf, encoding="utf-8")
    return pdf


# Team PDF report
@app.route('/teams.pdf')
def teams_pdf():
    teams = Team.query.all()
    team_report = render_template("team_report.html",
                                  teams=sorted(teams, key=by_team))
    pdf = create_pdf(team_report)
    response = make_response(pdf.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % \
                                              'teams.pdf'
    return response


# Ranks rerport in PDF
@app.route('/ranks.pdf')
def rank_pdf():
    teams = Team.query.all()
    for team in teams:
        sortTeamScores(team)
    ranks = render_template("ranks.html", teams=sorted(teams, key=by_team_best,
                                                       reverse=True))
    pdf = create_pdf(ranks)
    response = make_response(pdf.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % \
                                              'ranks.pdf'
    return response


# Calculate score totals for all scores for the team, and identify best
def sortTeamScores(team):
    for score in team.scores:
        score.total = score.getScore()
    if team.scores:
        team.best = max(team.scores, key=attrgetter('total'))
    else:
        team.best = None
    team.round1 = next((score for score in team.scores if
                        score.round_number == 1), None)
    team.round2 = next((score for score in team.scores if
                        score.round_number == 2), None)
    team.round3 = next((score for score in team.scores if
                        score.round_number == 3), None)


# Sort scores by total
def by_score(score):
    return score.total


# Sort teams by number
def by_team(team):
    return team.number


# Sort awards by name
def by_name(award):
    return award.name


# Sort teams by their best score total
def by_team_best(team):
    if team.best:
        return team.best.total
    else:
        return 0


# Utility method to get live score when score form is being filled out
@app.route('/_add_numbers')
def add_numbers():
    score = RobotScore(team=0,
                       round_number=0,
                       tree_branch_is_closer=request.args.get(
                           'tree_branch_is_closer') == 'true',
                       tree_branch_is_intact=request.args.get(
                           'tree_branch_is_intact') == 'true',
                       cargo_plane_location=request.args.get(
                           'cargo_plane_location', 0, type=int))

    return jsonify(result=score.getScore())


if __name__ == "__main__":
    app.debug = True
    db.create_all(app=app)
    app.run(debug=True)
