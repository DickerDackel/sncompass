#!/bin/env python3

import sys
import os
import json

from flask import Flask, jsonify, flash, render_template, url_for, request, redirect

from sncompass.calculate import distance_to, look_towards, look_origin
from tinysvg import SVG
from sncompass import Categories, Locations, LocationConflict

from form import CoordinateForm

app = Flask(__name__)
app.config.from_object('config')

locations = Locations()
categories = Categories()


def form_to_instructions(record):
    x = record['x']
    y = record['y']
    z = record['z']

    return {
        'x': x, 'y': y, 'z': z,
        'distance': distance_to(x, y, z),
        'surface_distance': distance_to(x, 0, z),
        'towards': look_towards(x, y, z),
        'reverse': look_origin(x, y, z),
        'name': record['name'] if record['name'] else '',
        'submitter': record['submitter'] if record['submitter'] else '',
    }

def svg_pointer(angle):
    svg = SVG(150, 150)
    cx, cy = 75, 75
    r = 50

    return '\n'.join([
        svg.line(x1=cx, y1=cy, x2=cx, y2=cy-r*0.8,
                 stroke='black', stroke_width='0.5mm',
                 transform=svg.transform([
                     svg.rotate(angle, cx, cy),
                 ])
                 ),
        svg.polyline(points=[(cx-5, cy), (cx, cy-10), (cx+5, cy), ],
                     stroke='black', stroke_width='0.12px',
                     stroke_miterlimit='miter',
                     transform=svg.transform([
                         svg.rotate(float(angle), cx, cy),
                         svg.translate(0, -r * 0.6),
                     ])
                     ),
    ])

import sys
from pprint import pprint

@app.route('/', methods=['GET', 'POST'])
def index():
    form = CoordinateForm()

    if request.method == 'GET' and 'id' in request.args:
        record = locations.by_id(request.args['id'])
        instructions = form_to_instructions(record)
    elif form.validate_on_submit():
        record = {
            'x': form.x.data,
            'y': form.y.data,
            'z': form.z.data,
            'name': form.name.data,
            'submitter': form.submitter.data,
        }
        instructions = form_to_instructions(record)

        if form.submitter.data and form.name.data:
            try:
                locations.add(record['x'], record['y'], record['z'],
                              record['name'], record['submitter'])
            except LocationConflict as e:
                flash(f'Location already saved as "{e.name}" at {e.location}', 'danger')
    else:
        instructions = None

        for err in form.errors:
            for details in form.errors[err]:
                flash(f'{err} failed - {details}', 'danger')

    if instructions:
        instructions['pointer'] = svg_pointer(instructions['towards'].angle)

    cat = categories.all()
    loc = locations.all()
    return render_template('index.html',
                           form=form,
                           instructions=instructions,
                           locations=loc,
                           categories=cat)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/license')
def license():
    return render_template('license.html')

@app.route('/delete/<id>')
def delete(id):
    locations.delete(id)

    return redirect(url_for('index'))

def create_app():
    return app

def main():
    app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == '__main__':
    main()
