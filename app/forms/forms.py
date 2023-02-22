from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email

from app import models


class RegisterForm(FlaskForm):
    email = StringField("Email",
                        validators=[DataRequired(), Email()])
    password = PasswordField("Password",
                             validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password",
                                     validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_email(self, email):
        user = models.User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class CandidateForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    position = SelectField("Position",
                           choices=["President", "Vice President", "Secretary"],
                           validators=[DataRequired()])
    profile_picture = FileField("Picture", validators=[FileAllowed(["jpg", "png"]), DataRequired()])
    submit = SubmitField("Add Candidate")


class PresidentVoteForm(FlaskForm):
    president = RadioField("Presidential", validators=[DataRequired()],
                           choices=[])
    submit_president = SubmitField('Vote')


class ViceVoteForm(FlaskForm):
    vice = RadioField("Vice Presidential", validators=[DataRequired()],
                      choices=[])
    submit_vice = SubmitField('Vote')


class SecretaryVoteForm(FlaskForm):
    secretary = RadioField("Secretarial", validators=[DataRequired()],
                           choices=[])
    submit_secretary = SubmitField('Vote')
