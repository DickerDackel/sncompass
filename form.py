from wtforms import IntegerField, SubmitField
from wtforms.validators import InputRequired
from flask_wtf import FlaskForm

class CoordinateForm(FlaskForm):
    x = IntegerField(label='x', default=0,
                     validators=[InputRequired()])
    y = IntegerField(label='y', default=0,
                     validators=[InputRequired()])
    z = IntegerField(label='z', default=0,
                     validators=[InputRequired()])
    show = SubmitField(label='Just Lead me!')

