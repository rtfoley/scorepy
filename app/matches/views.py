import csv
import os
from flask import Blueprint, flash, render_template, request, redirect, \
    url_for
from flask.ext.login import login_required
from app import db
from app.util import create_pdf
from models import Match, MatchSlot, CompetitionTable
from forms import UploadForm


mod_matches = Blueprint('matches', __name__, url_prefix='/matches')


# Match list
@mod_matches.route("/")
def index():
    matches = Match.query.all()
    return render_template("matches/match_list.html", matches=matches)
    
@mod_matches.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if request.method == 'POST' and 'file' in request.files:
        matchCount = 25

        flash('Imported %d matches' % matchCount, 'success')
        os.remove(filename)
        return redirect(url_for(".index"))
    return render_template("matches/match_upload_form.html", form=form)