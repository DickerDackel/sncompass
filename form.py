from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import InputRequired
from flask_wtf import FlaskForm

class CoordinateForm(FlaskForm):
    x = IntegerField(label='x', default=0,
                     validators=[InputRequired()])
    y = IntegerField(label='y', default=0,
                     validators=[InputRequired()])
    z = IntegerField(label='z', default=0,
                     validators=[InputRequired()])

    submitter = StringField(label='Submitted by')
    name = StringField(label='Location name')

    show = SubmitField(label='Lead me!')

