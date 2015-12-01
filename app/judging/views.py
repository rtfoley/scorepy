from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask.ext.login import login_required
from app import db
from app.teams.models import Team
from models import Presentation, Technical, CoreValues
from forms import PresentationForm, TechnicalForm, CoreValuesForm

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_judging = Blueprint('judging', __name__, url_prefix='/judging')


# Restrict access to authorized users only
@mod_judging.before_request
@login_required
def before_request():
    pass


@mod_judging.route("/")
def index():
    teams = Team.query.all()
    return render_template("judging/judging_list.html",
                           teams=sorted(teams, key=by_team))


# Add a presentation judging entry
@mod_judging.route('/judging/presentation/new', methods=['GET', 'POST'])
def add_presentation():
    form = PresentationForm()
    form.team_id.choices = [(t.id, t.number) for t in
                            sorted(Team.query.all(), key=by_team)]
    if request.method == 'POST' and form.validate_on_submit():
        presentation = Presentation()
        form.populate_obj(presentation)
        db.session.add(presentation)
        db.session.commit()
        return redirect(url_for(".index"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("judging/presentation_form.html", form=form)


# Edit a previously-entered presentation judging entry
@mod_judging.route("/judging/presentation/<int:presentation_id>/edit",
                   methods=['GET', 'POST'])
def edit_presentation(presentation_id):
    presentation = Presentation.query.get(presentation_id)
    form = PresentationForm(obj=presentation)
    del form.team_id

    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(presentation)
        db.session.commit()
        return redirect(url_for(".index"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("judging/presentation_form.html", form=form,
                           team_id=presentation.team_id)


# Delete a presentation judging entry
@mod_judging.route("/judging/presentation/<int:presentation_id>/delete",
                   methods=['GET', 'POST'])
def delete_presentation(presentation_id):
    presentation = Presentation.query.get(presentation_id)
    if request.method == 'POST':
        db.session.delete(presentation)
        db.session.commit()
        return redirect(url_for(".index"))
    return render_template("delete.html",
                           identifier="presentation evaluation for team %d"
                           % presentation.team.number)


# Add a technical judging entry
@mod_judging.route('/judging/technical/new', methods=['GET', 'POST'])
def add_technical():
    form = TechnicalForm()
    form.team_id.choices = [(t.id, t.number) for t in
                            sorted(Team.query.all(), key=by_team)]
    if request.method == 'POST' and form.validate_on_submit():
        technical = Technical()
        form.populate_obj(technical)
        db.session.add(technical)
        db.session.commit()
        return redirect(url_for(".index"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("judging/technical_form.html", form=form)


# Edit a previously-entered technical judging entry
@mod_judging.route("/judging/technical/<int:technical_id>/edit",
                   methods=['GET', 'POST'])
def edit_technical(technical_id):
    technical = Technical.query.get(technical_id)
    form = TechnicalForm(obj=technical)
    del form.team_id

    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(technical)
        db.session.commit()
        return redirect(url_for(".index"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("judging/technical_form.html", form=form,
                           team_id=technical.team_id)


# Delete a technical judging entry
@mod_judging.route("/judging/technical/<int:technical_id>/delete",
                   methods=['GET', 'POST'])
def delete_technical(technical_id):
    technical = Technical.query.get(technical_id)
    if request.method == 'POST':
        db.session.delete(technical)
        db.session.commit()
        return redirect(url_for(".index"))
    return render_template("delete.html",
                           identifier="technical evaluation for team %d"
                           % technical.team.number)


# Add a core values judging entry
@mod_judging.route('/judging/core_values/new', methods=['GET', 'POST'])
def add_core_values():
    form = CoreValuesForm()
    form.team_id.choices = [(t.id, t.number) for t in
                            sorted(Team.query.all(), key=by_team)]
    if request.method == 'POST' and form.validate_on_submit():
        core_values = CoreValues()
        form.populate_obj(core_values)
        db.session.add(core_values)
        db.session.commit()
        return redirect(url_for(".index"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("judging/core_values_form.html", form=form)


# Edit a previously-entered core values judging entry
@mod_judging.route("/judging/core_values/<int:core_values_id>/edit",
                   methods=['GET', 'POST'])
def edit_core_values(core_values_id):
    core_values = CoreValues.query.get(core_values_id)
    form = CoreValuesForm(obj=core_values)
    del form.team_id

    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(core_values)
        db.session.commit()
        return redirect(url_for(".index"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("judging/core_values_form.html", form=form,
                           team_id=core_values.team_id)


# Delete a core values judging entry
@mod_judging.route("/judging/core_values/<int:core_values_id>/delete",
                   methods=['GET', 'POST'])
def delete_core_values(core_values_id):
    core_values = CoreValues.query.get(core_values_id)
    if request.method == 'POST':
        db.session.delete(core_values)
        db.session.commit()
        return redirect(url_for(".index"))
    return render_template("delete.html",
                           identifier="core values evaluation for team %d"
                           % core_values.team.number)


# Sort teams by number
def by_team(team):
    return team.number
