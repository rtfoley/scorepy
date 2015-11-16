from flask.ext.wtf import Form
from wtforms import SelectField, RadioField
from .models import AwardCategory


# TODO add validation to ensure same award isn't assigned twice
class AwardWinnerForm(Form):
    # TODO these category constants should live separately
    category_id = SelectField(u'Award category',
                              choices=[(i.value, i.friendly_name) for i in AwardCategory],
                              coerce=int)
    place = RadioField(u'Place',
                       choices=[(0, '1st'), (1, '2nd'), (2, '3rd')],
                       default=0,
                       coerce=int)
    team_id = SelectField(u'Team', coerce=int)
