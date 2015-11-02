from flask import Blueprint, render_template

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_awards = Blueprint('awards', __name__, url_prefix='/awards')


# Awards page
@mod_awards.route("/", methods=['GET'])
def index():
    return render_template("awards/awards.html")
