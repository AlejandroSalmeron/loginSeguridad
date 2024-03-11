from wtforms import Form, validators
from wtforms import StringField, PasswordField, SubmitField


class LoginForm(Form):
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    submit = SubmitField('Iniciar sesión')

class AutForm(Form):
    codigo = StringField('Codigo', validators=[validators.DataRequired()])
    submit = SubmitField('Iniciar sesión')
