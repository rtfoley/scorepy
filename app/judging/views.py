from flask import Blueprint, render_template, request, redirect, flash, url_for
from app import db
from app.teams.models import Team
from models import Presentation, Technical, Teamwork, TeamSpirit
from forms import PresentationForm, TechnicalForm, TeamworkForm, TeamSpiritForm

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_judging = Blueprint('judging', __name__, url_prefix='/judging')


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


# Add a teamwork judging entry
@mod_judging.route('/judging/teamwork/new', methods=['GET', 'POST'])
def add_teamwork():
    form = TeamworkForm()
    form.team_id.choices = [(t.id, t.number) for t in
                            sorted(Team.query.all(), key=by_team)]
    if request.method == 'POST' and form.validate_on_submit():
        teamwork = Teamwork()
        form.populate_obj(teamwork)
        db.session.add(teamwork)
        db.session.commit()
        return redirect(url_for(".index"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("basic_form.html", form=form, title='Teamwork Form')


# Edit a previously-entered teamwork judging entry
@mod_judging.route("/judging/teamwork/<int:teamwork_id>/edit",
                   methods=['GET', 'POST'])
def edit_teamwork(teamwork_id):
    teamwork = Teamwork.query.get(teamwork_id)
    form = TeamworkForm(obj=teamwork)
    del form.team_id

    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(teamwork)
        db.session.commit()
        return redirect(url_for(".index"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("basic_form.html", form=form,
                           team_id=teamwork.team_id, title="Teamwork Form")


# Delete a teamwork judging entry
@mod_judging.route("/judging/teamwork/<int:teamwork_id>/delete",
                   methods=['GET', 'POST'])
def delete_teamwork(teamwork_id):
    teamwork = Teamwork.query.get(teamwork_id)
    if request.method == 'POST':
        db.session.delete(teamwork)
        db.session.commit()
        return redirect(url_for(".index"))
    return render_template("delete.html",
                           identifier="teamwork evaluation for team %d"
                           % teamwork.team.number)


# Add a team spirit judging entry
@mod_judging.route('/judging/team_spirit/new', methods=['GET', 'POST'])
def add_team_spirit():
    form = TeamSpiritForm()
    form.team_id.choices = [(t.id, t.number) for t in
                            sorted(Team.query.all(), key=by_team)]
    if request.method == 'POST' and form.validate_on_submit():
        team_spirit = TeamSpirit()
        form.populate_obj(team_spirit)
        db.session.add(team_spirit)
        db.session.commit()
        return redirect(url_for(".index"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("basic_form.html", form=form,
                           title='Team Spirit Form')


# Edit a previously-entered team spirit judging entry
@mod_judging.route("/judging/team_spirit/<int:team_spirit_id>/edit",
                   methods=['GET', 'POST'])
def edit_team_spirit(team_spirit_id):
    team_spirit = TeamSpirit.query.get(team_spirit_id)
    form = TeamSpiritForm(obj=team_spirit)
    del form.team_id

    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(team_spirit)
        db.session.commit()
        return redirect(url_for(".index"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("basic_form.html", form=form,
                           team_id=team_spirit.team_id,
                           title="Team Spirit Form")


# Delete a team spirit judging entry
@mod_judging.route("/judging/team_spirit/<int:team_spirit_id>/delete",
                   methods=['GET', 'POST'])
def delete_team_spirit(team_spirit_id):
    team_spirit = TeamSpirit.query.get(team_spirit_id)
    if request.method == 'POST':
        db.session.delete(team_spirit)
        db.session.commit()
        return redirect(url_for(".index"))
    return render_template("delete.html",
                           identifier="team spirit evaluation for team %d"
                           % team_spirit.team.number)


# Sort teams by number
def by_team(team):
    return team.number
