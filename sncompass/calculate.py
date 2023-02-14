#!/bin/env python3

import sys
import argparse
from collections import namedtuple

from math import sqrt, atan2, sin, cos, degrees, radians

Direction = namedtuple('Direction', ['orientation', 'tics', 'angle'])

def normalize_angle(angle):
    return angle - int(angle / 360) * 360

def angle_to_orientation(angle):
    # normalize angle
    angle = angle - int(angle / 360) * 360

    if -22.5 <= angle <= 22.5:
        return 'N'
    elif 22.5 <= angle <= 67.5:
        return 'NE'
    elif 67.5 <= angle <= 112.5:
        return 'E'
    elif 112.5 <= angle <= 157.5:
        return 'SE'
    elif 157.5 <= angle <= 202.5 or -202.5 <= angle <= -157.5:
        return 'S'
    elif 202.5 <= angle <= 247.5 or -157.5 <= angle <= -112.5:
        return 'SW'
    elif 247.5 <= angle <= 292.5 or -112.5 <= angle <= -67.5:
        return 'W'
    elif 292.5 <= angle <= 337.5 or -67.5 <= angle <= -22.5:
        return 'NW'
    elif 337.5 <= angle <= 360.0 or -22.5 <= angle <= 0.0:
        return 'N'
    else:
        return 'Unknown'

def angle_to_tics(angle):
    normalize = angle + 22.5
    offset = normalize % 45 - 22.5
    return int(offset / 7.5)

def coords_to_angle(x, z):
    return degrees(atan2(x, z))

def look_towards(x, y, z):
    angle = normalize_angle(coords_to_angle(x, z))

    return Direction(
        orientation=angle_to_orientation(angle),
        tics=angle_to_tics(angle),
        angle=angle
    )

def look_origin(x, y, z):
    angle = normalize_angle(coords_to_angle(x, z) + 180)

    return Direction(
        orientation=angle_to_orientation(angle),
        tics=angle_to_tics(angle),
        angle=angle
    )

def distance_to(x, y, z):
    return sqrt(x * x + y * y + z * z)


def calculate_all(x, y, z):
    return (
        distance_to(x, y, z),
        distance_to(x, 0, z),
        look_towards(x, y, z),
        look_origin(x, y, z),
    )

def test():
    l = 100
    for phi in range(0, 360, 9):
        rad = radians(phi)
        dx = l * sin(rad)
        dy = l * cos(rad)
        distance, surface_distance, direction, tics, angle = calculate_all(dx, 0, dy)
        print(f'{phi:3}: {dx:7.2f}, {dy:7.2f}: ', end='')
        print(f'{distance:.2f}m/{surface_distance:.2f}m {direction:>2s}{tics:+d} ({angle:7.2f}\u00b0)')

def render(distance, surface_distance, towards, reverse):
    print(f'Distance: {surface_distance:.2f}m ({distance:.2f}m) towards: {towards.orientation:>2s}{towards.tics:+d} ({towards.angle:.2f}\u00b0) reverse: {reverse.orientation:>2s}{reverse.tics:+d} ({reverse.angle:.2f}\u00b0)')

def main():
    cmdline = argparse.ArgumentParser(description='Calculate distance and direction from coordinates in Subnautica')
    cmdline.add_argument('x', type=int, help='X coordinate (E/W direction)')
    cmdline.add_argument('y', type=int, help='Y coordinate (depth)')
    cmdline.add_argument('z', type=int, help='Z coordinate (N/S direction)')
    cmdline.add_argument('-t', '--test', action='store_true', help='Run a circle test')
    opts = cmdline.parse_args(sys.argv[1:])

    if opts.test:
        start_angle = coords_to_angle(opts.x, opts.z)
        l = sqrt(opts.x * opts.x + opts.z * opts.z)
        for phi in range(0, 360, 9):
            rad = radians(normalize_angle(start_angle + phi))
            dx = l * sin(rad)
            dy = l * cos(rad)
            render(*calculate_all(dx, opts.y, dy))
    else:
        render(*calculate_all(opts.x, opts.y, opts.z))

if __name__ == '__main__':
    main()
