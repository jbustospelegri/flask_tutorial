from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length


class SignupForm(FlaskForm):
    # Flask ofrece formularios WTForms que permiten validar los datos introducidos por un usuario en un formulario.
    # Para ello es necesario heredar la clase FlaskForm y crear un formulario de este tipo en el html

    # Los WTForms ofrecidos por la librería permiten que se rendericen correctamente en formato html. De modo
    # que por ejemplo PasswordField creará un input de html en el cual los datos introducidos por el usuario estén
    # ocultos
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Registrar')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Recuerdame')
    submit = SubmitField('Login')