from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, validators, IntegerField


class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    remember_me = BooleanField('Remember me?', default=False)


class ChangePasswordForm(Form):
    old_password = PasswordField("Old password", [validators.DataRequired()])
    new_password = PasswordField("New password", [validators.DataRequired()])
    new_password_confirm = PasswordField("Confirm new password", [validators.DataRequired()])


class EventSettingsForm(Form):
    name = StringField('Event Name', [validators.DataRequired()])
    is_championship = BooleanField('Is Championship Event?', default=False)
    quarter_finals_teams = IntegerField('Teams in Quarter-Finals', default=8)
    semi_finals_teams = IntegerField('Teams in Semi-Finals', default=4)
    finals_teams = IntegerField('Teams in Finals', default=2)
