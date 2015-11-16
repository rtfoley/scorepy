from flask.ext.wtf import Form
from wtforms import SelectField, RadioField


# TODO add validation to ensure same award isn't assigned twice
class AwardWinnerForm(Form):
    # TODO these category constants should live separately
    category_id = SelectField(u'Award category',
                              choices=[(0, 'Champions Award'),
                                       (1, 'Research Award'),
                                       (2, 'Presentation Award'),
                                       (3, 'Innovative Solution Award'),
                                       (4, 'Mechanical Design Award'),
                                       (5, 'Programming Award'),
                                       (6, 'Strategy and Innovation Award'),
                                       (7, 'Teamwork Award'),
                                       (8, 'Inspiration Award'),
                                       (9, 'Team Spirit Award'),
                                       (10, 'Robot Performance Award')],
                              coerce=int)
    place = RadioField(u'Place',
                       choices=[(0, '1st'), (1, '2nd'), (2, '3rd')],
                       default=0,
                       coerce=int)
    team_id = SelectField(u'Team', coerce=int)
