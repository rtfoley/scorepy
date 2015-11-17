from flask.ext.wtf import Form
from wtforms import SelectField


# TODO add validation to ensure same award isn't assigned twice
class AwardWinnerForm(Form):
    team_id = SelectField(u'Team', coerce=int)
