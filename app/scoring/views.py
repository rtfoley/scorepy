from flask import Blueprint, render_template, request, flash, redirect, \
    url_for, jsonify
from app import db
from app.util import create_pdf
from app.teams.models import Team
from forms import ScoreForm
from models import RobotScore

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_scoring = Blueprint('scoring', __name__, url_prefix='/scores')


@mod_scoring.route("/")
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
def add():
    form = ScoreForm()
    form.team_id.choices = [(t.id, t.number) for t in
                            sorted(Team.query.all(), key=by_team)]

    if request.method == 'POST' and form.validate_on_submit():
        score = RobotScore(team=form.team_id.data,
                           round_number=form.round_number.data,

                           # M04 yellow/ blue bars
                           bars_in_west_transfer=form.bars_in_west_transfer.data,
                           bars_never_in_west_transfer=form.bars_never_in_west_transfer.data,

                           # M04 black bars
                           black_bars_in_original_position=form.black_bars_in_original_position.data,
                           black_bars_in_green_or_landfill=form.black_bars_in_green_or_landfill.data,
                           black_bars_elsewhere=form.black_bars_elsewhere.data,

                           # M02 Methane
                           methane_in_truck_or_factory=form.methane_in_truck_or_factory.data,

                           # M03 Transport
                           truck_supports_yellow_bin=form.truck_supports_yellow_bin.data == 'True',
                           yellow_bin_east_of_guide=form.yellow_bin_east_of_guide.data == 'True',

                           # M05 Careers
                           anyone_in_sorter_area=form.anyone_in_sorter_area.data == 'True',

                           # M06 Scrap Cars
                           engine_installed=form.engine_installed.data == 'True',
                           car_folded_in_east_transfer=form.car_folded_in_east_transfer.data == 'True',
                           car_never_in_safety=form.car_never_in_safety.data == 'True',

                           # M08 Composting
                           compost_ejected_not_in_safety=form.compost_ejected_not_in_safety.data == 'True',
                           compost_ejected_in_safety=form.compost_ejected_in_safety.data == 'True',

                           # M07 Cleanup
                           plastic_bags_in_safety=form.plastic_bags_in_safety.data,
                           animals_in_circles_without_bags=form.animals_in_circles_without_bags.data,
                           chicken_in_small_landfill_circle=form.chicken_in_small_landfill_circle.data == 'True',

                           # M10 Demolition
                           all_beams_not_in_setup_position=form.all_beams_not_in_setup_position.data == 'True',

                           # M01 Recycled Material
                           green_bins_in_opp_safety=form.green_bins_in_opp_safety.data,
                           opp_green_bins_in_safety=form.opp_green_bins_in_safety.data,

                           # M09 Salvage
                           valuables_in_safety=form.valuables_in_safety.data == 'True',

                           # M11 Purchasing Decisions
                           planes_in_safety=form.planes_in_safety.data,

                           # M12 Repurposing
                           compost_in_toy_package=form.compost_in_toy_package.data == 'True',
                           package_in_original_condition=form.package_in_original_condition.data == 'True')
        db.session.add(score)
        db.session.commit()
        return redirect(url_for(".index"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("scoring/score_form.html", form=form)


# Edit a previously-entered score
@mod_scoring.route("/<int:score_id>/edit", methods=['GET', 'POST'])
def edit(score_id):
    score = RobotScore.query.get(score_id)
    form = ScoreForm(obj=score)
    del form.team_id
    del form.round_number

    if request.method == 'POST' and form.validate_on_submit():
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

        db.session.commit()
        return redirect(url_for(".index"))
    elif request.method == 'POST':
        flash('Failed validation')
    return render_template("scoring/score_form.html",
                           form=form,
                           team_id=score.team_id,
                           round_number=score.round_number)


# Delete a score
@mod_scoring.route("/<int:score_id>/delete", methods=['GET', 'POST'])
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


# Sort teams by number
def by_team(team):
    return team.number


# Sort teams by their best score total
def by_team_best(team):
    if team.best:
        return team.best.total
    else:
        return 0
