from flask.ext.wtf import Form
from wtforms import FileField, validators


class UploadForm(Form):
    file = FileField(u'', [validators.regexp(u'^.*\.csv$')])