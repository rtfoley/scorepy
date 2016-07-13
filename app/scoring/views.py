from flask import Blueprint, render_template, request, flash, redirect, \
    url_for, jsonify
from flask.ext.login import login_required
from app import db
from app.util import create_pdf, sortTeamsWithPlaceholder
from app.teams.models import Team
from forms import ScoreForm
from models import RobotScore

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_scoring = Blueprint('scoring', __name__, url_prefix='/scores')


@mod_scoring.route("/")
@login_required
def index():
    teams = Team.query.all()
    return render_template("scoring/score_list.html",
                           teams=sorted(teams, key=by_team))


# Ranks rerport in PDF
@mod_scoring.route('/ranks.pdf')
def ranks_pdf():
    teams = Team.query.all()
    ranked_teams = sorted(teams, key=by_team_best, reverse=True)
    for i, team in enumerate(ranked_teams):
        team.rank = i + 1

    ranks = render_template("scoring/ranks.html", teams=ranked_teams)
    pdf = create_pdf(ranks, 'ranks.pdf')
    return pdf


# API endpoint providing rank data for the pit display
@mod_scoring.route("/api")
def api():
    # Get and sort the teams by rank
    teams = Team.query.all()
    ranked_teams = sorted(teams, key=by_team_best, reverse=True)

    # build the JSON data
    data = []
    for i, team in enumerate(ranked_teams):
        data.append({
            "number": team.number,
            "name": team.name,
            "affiliation": team.affiliation,
            "round1": team.round1.total if team.round1 is not None else "",
            "round2": team.round2.total if team.round2 is not None else "",
            "round3": team.round3.total if team.round3 is not None else "",
            "bestScore": team.best.total if team.best is not None else "",
            "rank": i + 1
        })

    return jsonify(ranks=data)


# Add a new robot score
@mod_scoring.route("/add", methods=['GET', 'POST'])
@login_required
def add():
    teams = Team.query.all()
    form = ScoreForm()

    form.team_id.choices = [(t.id, t.number) for t in
                            sortTeamsWithPlaceholder(teams)]

    # don't allow playoff round options during qualifying, or qualifying during playoffs
    if any(team.highest_round_reached > 3 for team in teams):
        form.round_number.choices = [(-1, 'Select'), (1, '1'), (2, '2'), (3, '3'), (4, 'Quarterfinals'), (5, 'Semifinals'), (6, 'Finals')]
    else:
        form.round_number.choices = [(-1, 'Select'), (1, '1'), (2, '2'), (3, '3')]

    # Gather and preset the team ID and round number fields if provided in URL
    preselected_team = request.args.get('team_id', default=None, type=int)
    preselected_round = request.args.get('round', default=None, type=int)
    if preselected_team is not None and request.method == 'GET':
        form.team_id.data = preselected_team

    if preselected_round is not None and request.method == 'GET':
        form.round_number.data = preselected_round

    repeat = request.args.get('repeat', default=False, type=bool)

    if request.method == 'POST' and request.form['end'] == 'reset':
        return redirect(url_for(".add", round = preselected_round, repeat = True))
    elif request.method == 'POST' and request.form['end'] == 'submit' and form.validate_on_submit():
        score = RobotScore(team=form.team_id.data,
                           round_number=form.round_number.data)
        populate_score(score, form)
        db.session.add(score)
        db.session.commit()
        if repeat:
            flash('Added score for %s round %s' % (score.team.number, score.round_number), 'success')
            return redirect(url_for(".add", round = preselected_round, repeat = True))
        else:
            if form.round_number.data <= 3:
                return redirect(url_for("review"))
            else:
                return redirect(url_for(".playoffs"))
    elif request.method == 'POST':
        flash('Failed validation', 'danger alert-auto-dismiss')
    return render_template("scoring/score_form.html",
                           form=form,
                           id=None,
                           repeat=repeat)


# Edit a previously-entered score
@mod_scoring.route("/<int:score_id>/edit", methods=['GET', 'POST'])
@login_required
def edit(score_id):
    score = RobotScore.query.get(score_id)
    form = ScoreForm(obj=score)
    del form.team_id
    del form.round_number

    if request.method == 'POST' and form.validate_on_submit():
        populate_score(score, form)
        db.session.commit()
        if score.round_number <= 3:
            return redirect(url_for("review"))
        else:
            return redirect(url_for(".playoffs"))
    elif request.method == 'POST':
        flash('Failed validation', 'danger alert-auto-dismiss')
    return render_template("scoring/score_form.html",
                           form=form,
                           team_id=score.team.number,
                           round_number=score.round_number,
                           id=score.id)


# Delete a score
@mod_scoring.route("/<int:score_id>/delete", methods=['GET', 'POST'])
@login_required
def delete(score_id):
    score = RobotScore.query.get(score_id)
    if request.method == 'POST':
        db.session.delete(score)
        db.session.commit()
        if score.round_number <= 3:
            return redirect(url_for("review"))
        else:
            return redirect(url_for(".playoffs"))
    return render_template("delete.html",
                           identifier="%s score for team %d" % (get_round_name(score.round_number), score.team.number))


# Playoffs page
@mod_scoring.route("/playoffs", methods=['GET'])
@login_required
def playoffs():
    quarterfinal_teams = Team.query.filter(Team.highest_round_reached >= 4)
    semifinal_teams = Team.query.filter(Team.highest_round_reached >= 5)
    final_teams = Team.query.filter(Team.highest_round_reached >= 6)
    return render_template("scoring/playoffs.html", quarterfinal_teams=quarterfinal_teams,
                           semifinal_teams=semifinal_teams, final_teams=final_teams)


@mod_scoring.route("/playoffs/<int:selected_round>/populate", methods=['GET', 'POST'])
@login_required
def populate(selected_round):
    if request.method == 'POST':
        if selected_round == 4:
            top_teams = sorted(Team.query.all(), key=by_team_best, reverse=True)[:8]
            for team in top_teams:
                team.highest_round_reached = 4
            db.session.commit()
        elif selected_round == 5:
            top_teams = sorted(Team.query.filter(Team.highest_round_reached >= 4), key=by_quarterfinal, reverse=True)[
                        :4]
            for team in top_teams:
                team.highest_round_reached = 5
            db.session.commit()
        elif selected_round == 6:
            top_teams = sorted(Team.query.filter(Team.highest_round_reached >= 5), key=by_semifinal, reverse=True)[:2]
            for team in top_teams:
                team.highest_round_reached = 6
            db.session.commit()
        return redirect(url_for(".playoffs"))
    else:
        # Check if all data has been entered for previous rounds
        previous_round = 0
        incomplete_data = None
        if selected_round == 4:
            previous_round = "qualifying"
            teams = Team.query.all()
            if any(len(team.qualifying_scores) != 3 for team in teams):
                incomplete_data = True
        elif selected_round == 5:
            previous_round = get_round_name(4)
            if any(team.quarterfinal is None for team in Team.query.filter(Team.highest_round_reached == 4)):
                incomplete_data = True
        elif selected_round == 6:
            previous_round = get_round_name(5)
            if any(team.semifinal is None for team in Team.query.filter(Team.highest_round_reached == 5)):
                incomplete_data = True

        return render_template("scoring/populate_playoffs.html",
                               round=get_round_name(selected_round),
                               previous_round=previous_round,
                               incomplete_data=incomplete_data)


@mod_scoring.route("/playoffs/<int:selected_round>/clear", methods=['GET', 'POST'])
@login_required
def clear_round(selected_round):
    if request.method == 'POST':
        # clear all scores for this round and any future round
        scores = RobotScore.query.filter(RobotScore.round_number >= selected_round)
        for score in scores:
            db.session.delete(score)

        # reset 'highest round reached' field for teams in this round or future rounds
        teams = Team.query.filter(Team.highest_round_reached >= selected_round)
        for team in teams:
            if team.highest_round_reached == 4:
                team.highest_round_reached = 0
            else:
                team.highest_round_reached = selected_round - 1
        db.session.commit()
        return redirect(url_for(".playoffs"))
    return render_template("scoring/clear_round.html", identifier=get_round_name(selected_round))


# Utility method to get live score when score form is being filled out
@mod_scoring.route('/_add_numbers')
def add_numbers():
    score = RobotScore(team=0,
                       round_number=0,

                       # M04 yellow/ blue bars
                       bars_in_west_transfer=request.args.get('bars_in_west_transfer', 0, type=int),
                       bars_never_in_west_transfer=request.args.get('bars_never_in_west_transfer', 0, type=int),

                       # M04 black bars
                       black_bars_in_original_position=request.args.get('black_bars_in_original_position', 0, type=int),
                       black_bars_in_green_or_landfill=request.args.get('black_bars_in_green_or_landfill', 0, type=int),
                       black_bars_elsewhere=request.args.get('black_bars_elsewhere', 0, type=int),

                       # M02 Methane
                       methane_in_truck_or_factory=request.args.get('methane_in_truck_or_factory', 0, type=int),

                       # M03 Transport
                       truck_supports_yellow_bin=request.args.get('truck_supports_yellow_bin') == 'True',
                       yellow_bin_east_of_guide=request.args.get('yellow_bin_east_of_guide') == 'True',

                       # M05 Careers
                       anyone_in_sorter_area=request.args.get('anyone_in_sorter_area') == 'True',

                       # M06 Scrap Cars
                       engine_installed=request.args.get('engine_installed') == 'True',
                       car_folded_in_east_transfer=request.args.get('car_folded_in_east_transfer') == 'True',
                       car_never_in_safety=request.args.get('car_never_in_safety') == 'True',

                       # M08 Composting
                       compost_ejected_not_in_safety=request.args.get('compost_ejected_not_in_safety') == 'True',
                       compost_ejected_in_safety=request.args.get('compost_ejected_in_safety') == 'True',

                       # M07 Cleanup
                       plastic_bags_in_safety=request.args.get('plastic_bags_in_safety', 0, type=int),
                       animals_in_circles_without_bags=request.args.get('animals_in_circles_without_bags', 0, type=int),
                       chicken_in_small_landfill_circle=request.args.get('chicken_in_small_landfill_circle') == 'True',

                       # M10 Demolition
                       all_beams_not_in_setup_position=request.args.get('all_beams_not_in_setup_position') == 'True',

                       # M01 Recycled Material
                       green_bins_in_opp_safety=request.args.get('green_bins_in_opp_safety', 0, type=int),
                       opp_green_bins_in_safety=request.args.get('opp_green_bins_in_safety', 0, type=int),

                       # M09 Salvage
                       valuables_in_safety=request.args.get('valuables_in_safety') == 'True',

                       # M11 Purchasing Decisions
                       planes_in_safety=request.args.get('planes_in_safety', 0, type=int),

                       # M12 Repurposing
                       compost_in_toy_package=request.args.get('compost_in_toy_package') == 'True',
                       package_in_original_condition=request.args.get('package_in_original_condition') == 'True')
    return jsonify(result=score.total)


# Populate a score object from form data
# TODO this could be removed by creating a custom form field for the select-button-group fields
def populate_score(score, form):
    # M04 yellow/ blue bars
    score.bars_in_west_transfer = form.bars_in_west_transfer.data
    score.bars_never_in_west_transfer = form.bars_never_in_west_transfer.data

    # M04 black bars
    score.black_bars_in_original_position = form.black_bars_in_original_position.data
    score.black_bars_in_green_or_landfill = form.black_bars_in_green_or_landfill.data
    score.black_bars_elsewhere = form.black_bars_elsewhere.data

    # M02 Methane
    score.methane_in_truck_or_factory = form.methane_in_truck_or_factory.data

    # M03 Transport
    score.truck_supports_yellow_bin = form.truck_supports_yellow_bin.data == 'True'
    score.yellow_bin_east_of_guide = form.yellow_bin_east_of_guide.data == 'True'

    # M05 Careers
    score.anyone_in_sorter_area = form.anyone_in_sorter_area.data == 'True'

    # M06 Scrap Cars
    score.engine_installed = form.engine_installed.data == 'True'
    score.car_folded_in_east_transfer = form.car_folded_in_east_transfer.data == 'True'
    score.car_never_in_safety = form.car_never_in_safety.data == 'True'

    # M08 Composting
    score.compost_ejected_not_in_safety = form.compost_ejected_not_in_safety.data == 'True'
    score.compost_ejected_in_safety = form.compost_ejected_in_safety.data == 'True'

    # M07 Cleanup
    score.plastic_bags_in_safety = form.plastic_bags_in_safety.data
    score.animals_in_circles_without_bags = form.animals_in_circles_without_bags.data
    score.chicken_in_small_landfill_circle = form.chicken_in_small_landfill_circle.data == 'True'

    # M10 Demolition
    score.all_beams_not_in_setup_position = form.all_beams_not_in_setup_position.data == 'True'

    # M01 Recycled Material
    score.green_bins_in_opp_safety = form.green_bins_in_opp_safety.data
    score.opp_green_bins_in_safety = form.opp_green_bins_in_safety.data

    # M09 Salvage
    score.valuables_in_safety = form.valuables_in_safety.data == 'True'

    # M11 Purchasing Decisions
    score.planes_in_safety = form.planes_in_safety.data

    # M12 Repurposing
    score.compost_in_toy_package = form.compost_in_toy_package.data == 'True'
    score.package_in_original_condition = form.package_in_original_condition.data == 'True'


# Sort teams by number
def by_team(team):
    return team.number


# Sort teams by their best score total
def by_team_best(team):
    if team.best:
        return team.best.total
    else:
        return 0


def by_quarterfinal(team):
    if team.quarterfinal:
        return team.quarterfinal.total
    else:
        return 0


def by_semifinal(team):
    if team.semifinal:
        return team.semifinal.total
    else:
        return 0


def get_round_name(round_number):
    if round_number == 4:
        return "Quarterfinals"
    elif round_number == 5:
        return "Semifinals"
    elif round_number == 6:
        return "Finals"
    else:
        return "qualifying round %d" % round_number
