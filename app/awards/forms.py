from flask.ext.wtf import Form
from wtforms import SelectField, TextField, validators, SubmitField


class AwardCategoryForm(Form):
    name = TextField("Name", [validators.Required(),
                              validators.Length(min=1, max=50)])
    submit = SubmitField(u'Submit')


# TODO add validation to ensure same award isn't assigned twice
class AwardWinnerForm(Form):
    category_id = SelectField(u'Award category', coerce=int)
    place = SelectField(u'Place',
                        choices=[(0, '1st'), (1, '2nd'), (2, '3rd')],
                        coerce=int)
    team_id = SelectField(u'Team', coerce=int)
    submit = SubmitField(u'Submit')
