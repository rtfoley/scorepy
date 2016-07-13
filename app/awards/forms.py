from flask.ext.wtf import Form
from wtforms import SelectField


# TODO add validation to ensure same award isn't assigned twice
class AwardWinnerForm(Form):
    team_id = SelectField(u'Team', coerce=int)

    def validate(self):
        # Base validation
        rv = Form.validate(self)
        if not rv:
            return False

        # Check for placeholder
        if self.team_id.data==-1:
            self.team_id.errors.append("Please select a team")
            return False

        return True
