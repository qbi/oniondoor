# -*- coding: utf-8 -*-
from __future__ import absolute_import

import pytimeparse
from flask import (Flask, flash, request, render_template, redirect,
                   url_for)

from door import DoorController

app = Flask(__name__, instance_relative_config=True)
# Load a config file from instance/config.py containing the app
# secret key: SECRET_KEY='<SECRET_KEY>'
app.config.from_pyfile('config.py')

door = DoorController(app)


@app.route('/')
def index():
    """Index page for the door system"""
    if door.is_activated():
        return render_template('index.tpl',
                               activated=True,
                               active_until=door.active_until,
                               active_until_human=door.active_until.humanize())
    else:
        return render_template('index.tpl',
                               activated=False)


@app.route('/activate', methods=['GET'])
def activate():
    """Endpoint to activate the door system

    Activate door for two minutes is no argument is provided. Otherwise
    parse the provided time period and activate for that period of time.
    """

    time_period = request.args.get('time')
    time_seconds = pytimeparse.parse(str(time_period))

    if not time_seconds or time_seconds <= 0:
        time_seconds = 2 * 60  # Default activation period of 2 minutes
        flash(u'Invalid time period provided', 'danger')
    else:
        flash(u'Door activated!', 'success')

    door.activate(time_seconds=time_seconds)

    return redirect(url_for('index'))


@app.route('/deactivate', methods=['GET'])
def deactivate():
    """Endpoint to deactivate the door system"""
    door.deactivate()
    flash(u'Door deactivated!', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
