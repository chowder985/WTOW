from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, DateField
from wtforms.validators import DataRequired


class StreamingForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    logo_url = StringField(
        'logo_url'
    )


class MovieForm(FlaskForm):
    title = StringField(
        'title', validators=[DataRequired()]
    )
    director = StringField(
        'director', validators=[DataRequired()]
    )
    poster_url = StringField(
        'poster_url'
    )
    release_date = DateField(
        'release_date',
        validators=[DataRequired()],
        default=date.today()
    )
    ott_platform = SelectMultipleField(
        'ott_platform',
        validators=[DataRequired()],
        validate_choice=False,
        choices=[]
    )
