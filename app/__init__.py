# Python library imports
import os, sys
from flask import Flask
from flask import render_template, redirect, url_for, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.login import login_user, logout_user, current_user
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import login_required
import logging
from logging.handlers import RotatingFileHandler

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app(config_object):
    # http://dev.prositen.com/wp/make-a-win32-exe-of-a-python-3-flask-app/
    # Fetch files from app directory by default, from script directory if code is frozen
    basedir = os.path.dirname(__file__)
    if getattr(sys, 'frozen', False):
        basedir = os.path.dirname(sys.executable)

    # Instruct Flask to load templates from the appropriate directories
    app = Flask(__name__,
                template_folder=os.path.join(basedir, 'templates'),
                static_folder=os.path.join(basedir, 'static'))

    # Setup application
    app.config.from_object(config_object)

    # Setup login manager

    login_manager.init_app(app)
    login_manager.login_view = "login"
    login_manager.login_message_category = "danger alert-auto-dismiss"

    # Setup password encryption
    bcrypt.init_app(app)

    # Setup logging
    handler = RotatingFileHandler(app.config['LOGGING_LOCATION'], maxBytes=10000, backupCount=1)
    handler.setLevel(app.config['LOGGING_LEVEL'])
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    # Setup database
    db.init_app(app)

    # Import a module / component using its blueprint handler variable (mod_auth)
    from app.teams.views import mod_teams as teams_module
    from app.scoring.views import mod_scoring as scoring_module
    from app.awards.views import mod_awards as awards_module
    from app.matches.views import mod_matches as matches_module

    # Register blueprint(s)
    app.register_blueprint(teams_module)
    app.register_blueprint(scoring_module)
    app.register_blueprint(awards_module)
    app.register_blueprint(matches_module)

    from models import User, EventSettings
    from forms import LoginForm, ChangePasswordForm, EventSettingsForm

    @login_manager.user_loader
    def load_user(userid):
        return User.query.filter(User.id == userid).first()


    @app.route("/")
    def index():
        return render_template("index.html")


    @app.route('/login', methods=["GET", "POST"])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is not None and user.is_correct_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get('next')

                # TODO should validate the next parameter before using it
                return redirect(next_page or url_for('index'))
            if user is None:
                form.username.errors.append("User does not exist")
            else:
                form.password.errors.append("Password is incorrect")

        return render_template('login.html', form=form)


    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))


    @app.route('/change_password', methods=["GET", "POST"])
    @login_required
    def change_password():
        form = ChangePasswordForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=current_user.username).first()
            if user.is_correct_password(form.old_password.data) and form.new_password.data == form.new_password_confirm.data:
                user.password = form.new_password.data
                db.session.commit()
                return redirect(url_for('index'))
            if not user.is_correct_password(form.old_password.data):
                form.old_password.errors.append("Old password is incorrect")
            if form.new_password.data != form.new_password_confirm.data:
                form.new_password.errors.append("New passwords do not match")
                form.new_password_confirm.errors.append("New passwords do not match")

        return render_template("change_password.html", form=form)


    # Pit Display page
    @app.route("/pit", methods=['GET'])
    def pit_display():
        title = EventSettings.query.first().name
        return render_template("pit_display.html", title=title, subtitle="Rankings")

    # Pit Display page
    @app.route("/settings", methods=["GET", "POST"])
    @login_required
    def settings():
        eventSettings = EventSettings.query.first()
        form = EventSettingsForm(obj = eventSettings)
        if request.method == 'POST' and form.validate_on_submit():
            form.populate_obj(eventSettings)
            db.session.commit()
            return redirect(url_for(".index"))
        elif request.method == 'POST':
            flash('Failed validation', 'danger alert-auto-dismiss')
        return render_template("settings.html", form=form)


    # Sample HTTP error handling
    @app.errorhandler(404)
    def not_found(error):
        app.logger.error('Page not found: %s', (request.path))
        return render_template('404.html'), 404


    @app.errorhandler(500)
    def internal_server_error(error):
        app.logger.error('Server Error: %s', (error))
        return render_template('500.html'), 500

    # Build the database:
    # This will create the database file using SQLAlchemy
    @app.before_first_request
    def setup_database():
        db.create_all()
        username = 'admin'
        if User.query.filter_by(username=username).first() is None:
            user = User("admin", "changeme")
            db.session.add(user)
            db.session.commit()
            
        if EventSettings.query.first() is None:
            eventSettings = EventSettings('Maine FLL Qualifier', False)
            db.session.add(eventSettings)
            db.session.commit()

    from app.teams.models import Team

    # Pit Display page
    @app.route("/review", methods=['GET'])
    @login_required
    def review():
        teams = Team.query.all()

        if not teams:
            return render_template("no_teams.html")

        return render_template("review.html",
                               teams=sorted(teams, key=by_team))

    # Sort teams by number
    def by_team(team):
        return team.number

    return app
