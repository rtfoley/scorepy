from flask import Blueprint, render_template, flash, request, redirect, \
    url_for
from app import db
from app.teams.models import Team
from models import AwardWinner, AwardCategory
from forms import AwardWinnerForm

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_awards = Blueprint('awards', __name__, url_prefix='/awards')


# Awards page
@mod_awards.route("/", methods=['GET'])
def index():
    award_winners = AwardWinner.query.all()
    # TODO sort by award category then place
    award_winners = sorted(award_winners, key=winner_by_award_name)
    for winner in award_winners:
        winner.category_name = AwardCategory(winner.category_id).friendly_name
    return render_template("awards/awards.html", award_winners=award_winners)


# Add a new award winner
@mod_awards.route("/add", methods=['GET', 'POST'])
def add_award_winner():
    form = AwardWinnerForm()
    form.team_id.choices = [(t.id, t.number) for t in
                            sorted(Team.query.all(), key=by_team)]

    if request.method == 'POST' and form.validate_on_submit():
        award_winner = AwardWinner()
        form.populate_obj(award_winner)
        db.session.add(award_winner)
        db.session.commit()
        return redirect(url_for(".index"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("basic_form.html", form=form,
                           title="Award Winner Form")


# Edit a previously-entered award winner
@mod_awards.route("/<int:award_winner_id>/edit", methods=['GET', 'POST'])
def edit_award_winner(award_winner_id):
    award_winner = AwardWinner.query.get(award_winner_id)
    form = AwardWinnerForm(obj=award_winner)
    form.team_id.choices = [(t.id, t.number) for t in
                            sorted(Team.query.all(), key=by_team)]

    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(award_winner)
        db.session.commit()
        return redirect(url_for(".index"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("basic_form.html", form=form,
                           title="Award Winner Form")


# Delete an award winner
@mod_awards.route("/<int:award_winner_id>/delete", methods=['GET', 'POST'])
def delete_award_winner(award_winner_id):
    award_winner = AwardWinner.query.get(award_winner_id)
    if request.method == 'POST':
        db.session.delete(award_winner)
        db.session.commit()
        return redirect(url_for(".index"))
    return render_template("delete.html", identifier="award winner for %s by team %d"
                           % (AwardCategory(award_winner.category_id).friendly_name, award_winner.team.number))


@mod_awards.route("/populate_slots", methods=['GET', 'POST'])
def populate_slots():
    if request.method == 'POST':
        # TODO populate award winner slots
        flash("Populated slots")
        return redirect(url_for(".index"))
    return render_template("awards/populate_slots.html")


# Sort teams by number
def by_team(team):
    return team.number


# Sort awards by name
def by_name(award):
    return award.name


# Sort award winners by category
def winner_by_award_name(award_winner):
    return award_winner.category_id
