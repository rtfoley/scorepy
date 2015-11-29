# Python library imports
from flask import Flask
from flask import render_template, redirect, url_for, flash
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.login import login_user, logout_user
from flask.ext.bcrypt import Bcrypt

# Setup application
app = Flask(__name__)
app.config.from_object('config')

# Setup login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Setup password encryption
bcrypt = Bcrypt(app)

# Setup database
db = SQLAlchemy(app)
db.init_app(app)


from models import User
from forms import LoginForm


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
            login_user(user)
            return redirect(url_for('index'))
        if user is None:
            form.username.errors.append("User does not exist")
        else:
            form.password.errors.append("Password is incorrect")

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('index'))


# Playoffs page
@app.route("/playoffs", methods=['GET'])
def playoffs():
    return render_template("playoffs.html")


# Pit Display page
@app.route("/pit", methods=['GET'])
def pit_display():
    return render_template("pit_display.html", title="Southern Maine FLL Qualifier", subtitle="Rankings")


# Pit Display page
@app.route("/settings", methods=['GET'])
def settings():
    return render_template("settings.html")


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# Import a module / component using its blueprint handler variable (mod_auth)
from app.teams.views import mod_teams as teams_module
from app.scoring.views import mod_scoring as scoring_module
from app.judging.views import mod_judging as judging_module
from app.awards.views import mod_awards as awards_module


# Register blueprint(s)
app.register_blueprint(teams_module)
app.register_blueprint(scoring_module)
app.register_blueprint(judging_module)
app.register_blueprint(awards_module)


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
