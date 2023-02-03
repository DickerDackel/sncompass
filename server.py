#!/bin/env python3

import sys
from flask import Flask, flash, render_template, url_for

import subnautica

from form import CoordinateForm

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = CoordinateForm()

    if form.validate_on_submit():
        x = form.x.data
        y = form.y.data
        z = form.z.data

        instructions = {
            'x': x, 'y': y, 'z': z,
            'distance': subnautica.distance(x, y, z),
            'surface_distance': subnautica.surface_distance(x, y, z),
            'towards': subnautica.look_towards(x, y, z),
            'reverse': subnautica.look_origin(x, y, z),
        }
    else:
        for err in form.errors:
            for details in form.errors[err]:
                flash(f'{err} failed - {details}', 'danger')
        instructions = None

    return render_template('index.html', form=form, instructions=instructions)

def create_app():
    app.config.from_object('config')
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8080, debug=True)
