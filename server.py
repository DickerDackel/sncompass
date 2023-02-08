#!/bin/env python3

import sys
import os
import datetime
import json

from flask import Flask, jsonify, flash, render_template, url_for

import subnautica

from form import CoordinateForm

app = Flask(__name__)

class LocationConflict(BaseException):
    def __init__(self, message, name, location):
        super().__init__(self, message)
        self.name = name
        self.location = location

class Locations:
    def __init__(self, fname):
        self.fname = fname
        self.locations = self.load()

    def load(self):
        try:
            with open(self.fname, 'r') as f:
                return(json.load(f))
        except (OSError, json.JSONDecodeError):
            return []

    def save(self):
        try:
            os.rename(self.fname, self.fname + '.bak')
        except FileNotFoundError:
            pass

        with open(self.fname, 'w') as f:
            json.dump(self.locations, f)

    def add(self, name, submitter, x, y, z):
        for l in self.locations:
            if x - 10 <= l['x'] <= x + 10 and y - 10 <= l['y'] <= y + 10 and z - 10 <= l['z'] <= z + 10:
                raise LocationConflict('Location conflict', l['name'], (l['x'], l['y'], l['z']))

        self.locations.append({
            'name': name, 'submitter': submitter,
            'x': x, 'y': y, 'z': z,
            'created': datetime.datetime.isoformat(datetime.datetime.now()),
        })

        self.save()

def form_to_instructions(form):
    x = form.x.data
    y = form.y.data
    z = form.z.data

    return {
        'x': x, 'y': y, 'z': z,
        'distance': subnautica.distance_to(x, y, z),
        'surface_distance': subnautica.distance_to(x, 0, z),
        'towards': subnautica.look_towards(x, y, z),
        'reverse': subnautica.look_origin(x, y, z),
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    form = CoordinateForm()

    locations = Locations('locations.json')

    if form.validate_on_submit():
        instructions = form_to_instructions(form)

        if form.submitter.data and form.name.data:
            try:
                locations.add(
                    name=form.name.data, submitter=form.submitter.data,
                    x=form.x.data, y=form.y.data, z=form.z.data)
            except LocationConflict as e:
                flash(f'Location already saved as "{e.name}" at {e.location}', 'danger')
    else:
        for err in form.errors:
            for details in form.errors[err]:
                flash(f'{err} failed - {details}', 'danger')
        instructions = None

    return render_template('index.html', form=form, instructions=instructions, locations=locations.locations)

@app.route('/why')
def why():
    return render_template('why.html')

def create_app():
    app.config.from_object('config')
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8080, debug=True)
