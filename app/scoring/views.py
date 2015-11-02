from flask import Blueprint, render_template, request, flash, redirect, \
    url_for, jsonify, make_response
from app import db
from app.util import create_pdf
from app.teams.models import Team
from forms import ScoreForm
from models import RobotScore
from operator import attrgetter


# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_scoring = Blueprint('scoring', __name__, url_prefix='/scores')


@mod_scoring.route("/")
def index():
    teams = Team.query.all()
    for team in teams:
        sortTeamScores(team)
    return render_template("scoring/score_list.html",
                           teams=sorted(teams, key=by_team))


# Ranks rerport in PDF
@mod_scoring.route('/ranks.pdf')
def ranks_pdf():
    teams = Team.query.all()
    for team in teams:
        sortTeamScores(team)
    ranks = render_template("scoring/ranks.html",
                            teams=sorted(teams, key=by_team_best,
                                         reverse=True))
    pdf = create_pdf(ranks)
    response = make_response(pdf.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % \
                                              'ranks.pdf'
    return response


# Add a new robot score
@mod_scoring.route("/scores/new", methods=['GET', 'POST'])
def add():
    form = ScoreForm()
    form.team_id.choices = [(t.id, t.number) for t in
                            sorted(Team.query.all(), key=by_team)]

    if request.method == 'POST' and form.validate_on_submit():
        score = RobotScore()
        form.populate_obj(score)
        db.session.add(score)
        db.session.commit()
        return redirect(url_for(".index"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("scoring/score_form.html", form=form)


# Edit a previously-entered score
@mod_scoring.route("/scores/<int:score_id>/edit", methods=['GET', 'POST'])
def edit(score_id):
    score = RobotScore.query.get(score_id)
    form = ScoreForm(obj=score)
    del form.team_id
    del form.round_number

    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(score)
        db.session.commit()
        return redirect(url_for(".index"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("scoring/score_form.html",
                           form=form,
                           team_id=score.team_id,
                           round_number=score.round_number)


# Delete a score
@mod_scoring.route("/scores/<int:score_id>/delete", methods=['GET', 'POST'])
def delete(score_id):
    score = RobotScore.query.get(score_id)
    if request.method == 'POST':
        db.session.delete(score)
        db.session.commit()
        return redirect(url_for(".index"))
    return render_template("delete.html", identifier="score for %d in round %d"
                           % (score.team.number, score.round_number))


# Utility method to get live score when score form is being filled out
@mod_scoring.route('/_add_numbers')
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


# Sort teams by number
def by_team(team):
    return team.number


# Sort teams by their best score total
def by_team_best(team):
    if team.best:
        return team.best.total
    else:
        return 0
