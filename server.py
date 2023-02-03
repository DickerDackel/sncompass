#!/bin/env python3

import sys
from pprint import pformat
from flask import Blueprint, Flask, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
import wtforms.validators

import subnautica

class CoordinateForm(FlaskForm):
    x = IntegerField(label='x', default=0,
                     validators=[wtforms.validators.InputRequired()])
    y = IntegerField(label='y', default=0,
                     validators=[wtforms.validators.InputRequired()])
    z = IntegerField(label='z', default=0,
                     validators=[wtforms.validators.InputRequired()])
    submit = SubmitField(label='Lead me!')

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = CoordinateForm()

    if form.validate_on_submit():
        x = form.x.data
        y = form.y.data
        z = form.z.data

        instructions = {
            'distance': subnautica.distance(x, y, z),
            'surface_distance': subnautica.surface_distance(x, y, z),
            'towards': subnautica.look_towards(x, y, z),
            'reverse': subnautica.look_origin(x, y, z),
        }
    else:
        instructions = None

    return render_template('index.html', form=form, instructions=instructions)

def main():
    app.config.from_object('config')
    app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == '__main__':
    main()
