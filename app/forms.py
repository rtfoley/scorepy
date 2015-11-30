from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, validators


class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])


class ChangePasswordForm(Form):
    old_password = PasswordField("Old password", [validators.DataRequired()])
    new_password = PasswordField("New password", [validators.DataRequired()])
    new_password_confirm = PasswordField("Confirm new password", [validators.DataRequired()])
