
#    AutoTriops: An automated triops tank maintenance application
#    Copyright (C) 2013 C Nelson <cnelsonsic@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from flask import Blueprint, jsonify, render_template

from controllers import TankController, ParameterController

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
def do_dashboard():
    # Show current state of tanks and what needs done, health thereof, etc.
    # Also allow input of tank parameters via do_update
    pc = ParameterController()
    tc = TankController()

    # Get the raw parameters for display.
    out_params = dict()
    for tank, params in pc.get_params().iteritems():
        for param in params:
            if param.tank not in params:
                out_params[param.tank.name] = dict()
            out_params[param.tank.name][param.param.name] = param.value

    # Any immediate parameters in need of attention?
    alerts = dict()
    for tank in tc.get_tanks():
        if tank.name not in alerts:
            alerts[tank.name] = dict()

        for level, warnings in pc.get_alerts(tank.id).iteritems():
            if level not in alerts[tank.name]:
                alerts[tank.name][level] = dict()

            for param, warning in warnings.iteritems():
                alerts[tank.name][level][param.param.name] = warning

    return render_template('dashboard.html', params=out_params, alerts=alerts)

@dashboard.route('/update/<int:tank_id>', methods=['POST'])
def do_update():
    # Ajax handler that updates the database with tank parameters.
    pass

@dashboard.route('/favicon.ico')
def do_serve_favicon():
    import os
    from flask import send_from_directory, current_app, request

    ua = request.headers.get('User-Agent')
    if "Chrome" in ua or "Opera" in ua:
        # favicon = "triops.svg"
        favicon = "triops.png"
    elif "Firefox" in ua:
        favicon = "triops.png"
    else:
        favicon = "triops.ico"

    return send_from_directory(os.path.join(current_app.root_path, 'static'),
                               favicon)

@dashboard.route('/dedication')
def do_dedication():
    return("Dedicated to my very first triops. "
           "You ate all your friends, family, neighbors, "
           "your skin, and your own poop, "
           "but you were still my first.")
