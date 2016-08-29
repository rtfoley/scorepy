from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, validators


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