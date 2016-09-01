from flask.ext.wtf import Form
from wtforms import FileField, validators, SelectField


class UploadForm(Form):
    file = FileField(u'', [validators.regexp(u'^.*\.csv$')])
    

class AnnouncerDisplayForm(Form):
    match_id = SelectField(u'Match', coerce=int)