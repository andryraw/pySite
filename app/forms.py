from app import app
from app.models import User, Genre, Director
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField,\
    SubmitField, EmailField, SelectField, FileField
from wtforms.validators import InputRequired, Email, EqualTo, Length, ValidationError


# -------------------- user section --------------------

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired(), Email()])
    about_me = TextAreaField('About Me')
    password_1 = PasswordField('Password', validators=[InputRequired(), \
        Length(min=8, message='Password must be at least 8 characters long')])
    password_2 = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password_1')])
    submit = SubmitField('Registration')

    # Custom validators
    # password check on >=1 number and upper letter
    def validate_password_1(self, password_1):
        password = password_1.data
        if not any(char.isdigit() for char in password):
            raise ValidationError('Password should have at least one numeral')
        if not any(char.isupper() for char in password):
            raise ValidationError('Password should have at least one uppercase letter')

    def validate_username(self, username):
        u = User.query.filter_by(username=username.data).first()
        if u is not None:
            raise ValidationError('Please use a different username')

    def validate_email(self, email):
        u = User.query.filter_by(email=email.data).first()
        if u is not None:
            raise ValidationError('Please use a different email')


class EditForm(RegistrationForm):
    submit = SubmitField('Submit')

    def validate_username(self, username):
        pass

    def validate_email(self, email):
        pass


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Enter')


# -------------------- film section --------------------

class AddFilmForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    type = SelectField('Type', validators=[InputRequired()], choices=['Movie', 'TV series'])
    duration = StringField('Duration', validators=[InputRequired()])
    year = StringField('Year', validators=[InputRequired()])
    country = StringField('Country', validators=[InputRequired()])
    #director_list = Director.query.all()
    #director = SelectField('Director', choises=[*director_list])
    submit = SubmitField('Add')


class FilmPosterForm(FlaskForm):
    poster_loader = FileField('Poster')


class AddGenre(FlaskForm):
    name = StringField('Genre', validators=[InputRequired()])
    submit = SubmitField('Add')


class AddDirector(FlaskForm):
    name = StringField('Director', validators=[InputRequired()])
    submit = SubmitField('Add')

class AddFilmGenre(FlaskForm):
    #app.app_context().push()
    genres_list = Genre.query.order_by(Genre.name).all()
    genres = SelectField('Genre', choices=[*genres_list], coerce=str)
    submit = SubmitField('Add genre')


class AddFilmDirector(FlaskForm):
    #app.app_context().push()
    director_list = Director.query.order_by(Director.name).all()
    director = SelectField('Director', choices=[*director_list])
    submit = SubmitField('Add director')