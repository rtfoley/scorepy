# Python library imports
import flask
from flask import flash, render_template, request, jsonify, redirect, url_for, \
    make_response
from flask_bootstrap import Bootstrap
from cStringIO import StringIO
from xhtml2pdf import pisa
from operator import attrgetter

# Imports from other parts of the app
from forms import ScoreForm, TeamForm, PresentationForm
from models import RobotScore, Team, Presentation, db

# setup application
app = flask.Flask(__name__)
app.config.from_object('config')
Bootstrap(app)

db.init_app(app)


# Main route
@app.route("/")
def index():
    return render_template("index.html")


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
    return render_template("judging_list.html", teams=sorted(teams, key=by_team))


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


# Add a presentation judging evaluation
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
    return render_template("basic_form.html", form=form, title='Presentation Form')


# Edit a previously-entered score
@app.route("/judging/presentation/<int:presentation_id>/edit", methods=['GET', 'POST'])
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
    return render_template("basic_form.html", form=form, team_id=presentation.team_id,
                           title="Presentation Form")


# Delete a score
@app.route("/judging/presentation/<int:presentation_id>/delete", methods=['GET', 'POST'])
def delete_presentation(presentation_id):
    presentation = Presentation.query.get(presentation_id)
    if request.method == 'POST':
        db.session.delete(presentation)
        db.session.commit()
        return redirect(url_for("judging_list"))
    return render_template("delete.html", identifier="presentation evaluation for team %d"
                           % presentation.team.number)


# Return a list of scores, highest - lowest
@app.route("/ranks", methods=['GET'])
def ranks():
    teams = Team.query.all()
    for team in teams:
        sortTeamScores(team)
    return render_template("ranks.html", teams=sorted(teams, key=by_team_best,
                                                      reverse=True))


# Awards page
@app.route("/awards", methods=['GET'])
def awards():
    return render_template("awards.html")


# Create a PDF file from data
def create_pdf(pdf_data):
    pdf = StringIO()
    pisa.CreatePDF(StringIO(pdf_data.encode('utf-8')), pdf, encoding="utf-8")
    return pdf


# Ranks rerport in PDF
@app.route('/ranks.pdf')
def rank_pdf():
    pdf = create_pdf(ranks())
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
