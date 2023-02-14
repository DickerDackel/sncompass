#!/bin/env python3

import sys
import os
import datetime
import json

from flask import Flask, jsonify, flash, render_template, url_for, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

import subnautica
from svg import SVG

from form import CoordinateForm

app = Flask(__name__)
app.config.from_object('config')

class LocationConflict(BaseException):
    def __init__(self, message, name, location):
        super().__init__(self, message)
        self.name = name
        self.location = location

class Locations:
    def __init__(self, url):
        connect, db = url.rsplit('/', maxsplit=1)
        client = MongoClient(connect)

        self.db = client[db]

    @staticmethod
    def _gen_near_query(x, y, z):
        return {
            '$and': [
                {'x': {'$gte': x-10, '$lte': x+10}},
                {'y': {'$gte': y-10, '$lte': y+10}},
                {'z': {'$gte': z-10, '$lte': z+10}},
            ]
    }

    @staticmethod
    def _gen_exact_query(x, y, z):
        return {
            '$and': [
                {'x': {'$eq': x}},
                {'y': {'$eq': y}},
                {'z': {'$eq': z}},
            ]
    }

    def by_id(self, id):
        return self.db.locations.find_one({'_id': id})

    def find(self, x, y, z):
        return self.db.locations.find(Locations._gen_near_query(x, y, z)).sort('name')

    def has(self, x, y, z):
        return self.db.locations.count_documents(Locations._gen_near_query(x, y, z))

    def all(self):
        return self.db.locations.find({}).sort('name')

    def delete(self, id):
        res = self.db.locations.delete_one(
            {'$and': [
                {'x': {'$ne': 0}},
                {'y': {'$ne': 0}},
                {'z': {'$ne': 0}},
                {'_id': ObjectId(id)}
            ]}
        )

    def add(self, name, submitter, x, y, z):
        rec = {
            'name': name,
            'submitter': submitter,
            'x': x, 'y': y, 'z': z,
            'created': datetime.datetime.isoformat(datetime.datetime.now()),
        }

        match = list(self.find(x, y, z))
        if len(match):
            raise LocationConflict('Location conflict', match[0]['name'], (match[0]['x'], match[0]['y'], match[0]['z']))

        self.db.locations.insert_one(rec)

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
        'name': form.name.data if form.name.data else '',
        'submitter': form.submitter.data if form.submitter.data else '',
    }

def svg_pointer(angle):
    svg = SVG(150, 150)
    cx, cy = 75, 75
    r = 50

    app.logger.error(angle)

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

@app.route('/', methods=['GET', 'POST'])
def index():
    prefill = None
    if request.method == 'GET' and 'id' in request.args:
        app.logger.error('Got an ID: ' + request.args['id'])
        prefill = locations.by_id(ObjectId(request.args['id']))
        app.logger.error('Prefill: ' + repr(prefill))
        form = CoordinateForm(x=prefill['x'], y=prefill['y'], z=prefill['z'],
                              name=prefill['name'],
                              submitter=prefill['submitter'])
        app.logger.error(form)
    else:
        form = CoordinateForm()
        app.logger.error(form)

    if form.validate_on_submit() or prefill is not None:
        instructions = form_to_instructions(form)
        instructions['pointer'] = svg_pointer(instructions['towards'].angle)

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

    return render_template('index.html', form=form, instructions=instructions, locations=locations.all())

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

locations = Locations(app.config['MONGODB_URL'])

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8080, debug=True)
