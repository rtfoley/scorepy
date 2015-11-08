from flask.ext.wtf import Form
from wtforms import IntegerField, TextField, validators, SubmitField, FileField


class TeamForm(Form):
    number = IntegerField("Number", [validators.Required(),
                                     validators.NumberRange(min=1, max=99999)])
    name = TextField("Name", [validators.Required(),
                              validators.Length(min=1, max=50)])
    affiliation = TextField("Affiliation", [validators.Length(min=1, max=200)])
    city = TextField("City", [validators.Length(min=1, max=50)])
    state = TextField("State", [validators.Length(min=2, max=2)])


class UploadForm(Form):
    file = FileField(u'', [validators.regexp(u'^.*\.csv$')])
