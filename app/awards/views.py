from flask import Blueprint, render_template, flash, request, redirect, \
    url_for
from app import db
from app.teams.models import Team
from models import AwardCategory, AwardWinner
from forms import AwardCategoryForm, AwardWinnerForm

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_awards = Blueprint('awards', __name__, url_prefix='/awards')


# Awards page
@mod_awards.route("/", methods=['GET'])
def index():
    award_winners = AwardWinner.query.all()
    # TODO sort by award category then place
    return render_template("awards/awards.html",
                           award_winners=sorted(award_winners,
                                                key=winner_by_award_name))


# Add a team spirit judging entry
@mod_awards.route('/settings/award_categories/new', methods=['GET', 'POST'])
def add_award_category():
    form = AwardCategoryForm()
    if request.method == 'POST' and form.validate_on_submit():
        award_category = AwardCategory()
        form.populate_obj(award_category)
        db.session.add(award_category)
        db.session.commit()
        return redirect(url_for("settings"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("basic_form.html", form=form,
                           title='Award Category Form')


# Edit a previously-entered team spirit judging entry
@mod_awards.route("/settings/award_categories/<int:award_category_id>/edit",
                  methods=['GET', 'POST'])
def edit_award_category(award_category_id):
    award_category = AwardCategory.query.get(award_category_id)
    form = AwardCategoryForm(obj=award_category)

    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(award_category)
        db.session.commit()
        return redirect(url_for("settings"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("basic_form.html", form=form,
                           title="Award Category Form")


# Delete a team spirit judging entry
@mod_awards.route("/settings/award_categories/<int:award_category_id>/delete",
                  methods=['GET', 'POST'])
def delete_award_category(award_category_id):
    award_category = AwardCategory.query.get(award_category_id)
    if request.method == 'POST':
        db.session.delete(award_category)
        db.session.commit()
        return redirect(url_for("settings"))
    return render_template("delete.html",
                           identifier="award category '%s'"
                           % award_category.name)


# Add a new award winner
@mod_awards.route("/awards/add", methods=['GET', 'POST'])
def add_award_winner():
    form = AwardWinnerForm()
    form.category_id.choices = [(c.id, c.name) for c in
                                sorted(AwardCategory.query.all(), key=by_name)]
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
@mod_awards.route("/awards/<int:award_winner_id>/edit", methods=['GET', 'POST'])
def edit_award_winner(award_winner_id):
    award_winner = AwardWinner.query.get(award_winner_id)
    form = AwardWinnerForm(obj=award_winner)
    form.category_id.choices = [(c.id, c.name) for c in
                                sorted(AwardCategory.query.all(), key=by_name)]
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
@mod_awards.route("/awards/<int:award_winner_id>/delete", methods=['GET', 'POST'])
def delete_award_winner(award_winner_id):
    award_winner = AwardWinner.query.get(award_winner_id)
    if request.method == 'POST':
        db.session.delete(award_winner)
        db.session.commit()
        return redirect(url_for(".index"))
    return render_template("delete.html", identifier="award winner for %s by team %d"
                           % (award_winner.category.name, award_winner.team.number))


# Sort teams by number
def by_team(team):
    return team.number


# Sort awards by name
def by_name(award):
    return award.name


# Sort award winners by category
def winner_by_award_name(award_winner):
    return award_winner.category.name
