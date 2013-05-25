from flask import Blueprint, jsonify

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

    return jsonify(params=out_params, alerts=alerts)

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
