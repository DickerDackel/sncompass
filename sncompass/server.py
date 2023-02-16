#!/bin/env python3

from flask import Flask, flash, make_response, render_template, url_for, request, redirect

from sncompass import CoordinateForm, Categories, Locations, LocationConflict
from sncompass.calculate import distance_to, look_towards, look_origin

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

    cat = categories.all()
    loc = locations.all()
    return render_template('index.html',
                           form=form,
                           instructions=instructions,
                           locations=loc,
                           categories=cat)


@app.route('/compass/<float:angle>')
def compass(angle):
    # Compass dimensions:
    #   radius 75 (makes 150 diameter)
    #   the tics are arranged at a radius of 50px
    #   length of pointer: 80% of tic radius 50
    tic_radius = 50

    pointer_length = tic_radius * 0.8
    pointer_head = -tic_radius * 0.6

    res = make_response(
        render_template('compass.svg',
                        angle=angle,
                        pointer_length=pointer_length,
                        pointer_head=pointer_head),
    )
    res.content_type = 'image/svg+xml'
    return res


@app.route('/crosshair/<x>/<y>/<z>')
def crosshair(x, y, z):
    svg_x = ( float(x) + 2000) / 100
    svg_z = (-float(z) + 2000) / 100

    resp = make_response(
        render_template('SNMap-150.svg', x=svg_x, y=svg_z),
    )
    resp.content_type = 'image/svg+xml'
    return resp


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
