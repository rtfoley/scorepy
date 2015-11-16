from flask.ext.wtf import Form
from wtforms import IntegerField, StringField, validators, FileField, BooleanField


class TeamForm(Form):
    number = IntegerField("Number", [validators.DataRequired(),
                                     validators.NumberRange(min=1, max=99999)])
    name = StringField("Name", [validators.DataRequired(),
                                validators.Length(min=1, max=50)])
    affiliation = StringField("Affiliation", [validators.Length(min=1, max=200)])
    city = StringField("City", [validators.Length(min=1, max=50)])
    state = StringField("State", [validators.Length(min=2, max=2)])
    is_rookie = BooleanField("Rookie?")


class UploadForm(Form):
    file = FileField(u'', [validators.regexp(u'^.*\.csv$')])
