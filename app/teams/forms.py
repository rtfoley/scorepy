from flask.ext.wtf import Form
from wtforms import IntegerField, StringField, validators, FileField, BooleanField, SelectField
from .models import Team


class TeamForm(Form):
    number = IntegerField("Number", [validators.DataRequired(),
                                     validators.NumberRange(min=1, max=99999)])
    name = StringField("Name", [validators.DataRequired(),
                                validators.Length(min=1, max=50)])
    affiliation = StringField("Affiliation", [validators.Length(min=1, max=200)])
    city = StringField("City", [validators.Length(min=1, max=50)])
    state = StringField("State", [validators.Length(min=2, max=2)])
    is_rookie = BooleanField("Rookie?")

    def validate(self):
        # Base validation
        rv = Form.validate(self)
        if not rv:
            return False

        if not self.number:
            return True

        # validate that the team number isn't already being used
        t = Team.query.filter_by(number=self.number.data).first()
        if t is not None:
            self.number.errors.append("Team with this number already exists")
            return False

        # TODO validate that if the 'highest round reached' value is being decreased that there aren't existing scores for that round

        return True


class UploadForm(Form):
    file = FileField(u'', [validators.regexp(u'^.*\.csv$')])
