#!/bin/bash

gunicorn -w 4 --reload --bind 0.0.0.0:8080 'sncompass.server:create_app()'
