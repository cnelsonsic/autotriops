
from db import db
from models import Tank, TankParameter, Parameter

class TankController(object):

    def add_tank(self, name):
        tank = Tank(name)
        db.session.add(tank)
        db.session.commit()
        return tank

    def get_tanks(self):
        return Tank.query.all()

    def update_parameter(self, tank, param, value):
        tank = Tank.query.filter_by(id=tank).first()

        if tank:
            if isinstance(param, basestring):
                param = Parameter.query.filter_by(name=param).first()
            tp = TankParameter(param, value, tank)
            db.session.add(tp)
            db.session.commit()
            return True

    def get_latest_parameters(self, tank_id):
        tank = Tank.query.filter_by(id=tank_id).first()
        if tank:
            params = TankParameter.query.filter_by(tank=tank)\
                                        .order_by(TankParameter.timestamp)\
                                        .all()

            # TODO: Emulate GROUP BY in python here, by param
            return params

class ParameterController(object):
    def add_param(self, name, upper, lower, tolerance):
        param = Parameter.query.filter_by(name=name).first()
        if param:
            # Should just overwrite it.
            return param

        p = Parameter(name, upper, lower, tolerance)
        db.session.add(p)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        return p

    def get_params(self, tank=None):
        tc = TankController()
        parameters = {}

        if not tank:
            tanks = [t.id for t in tc.get_tanks()]
        else:
            tanks = [tank]

        parameters = {tank:tc.get_latest_parameters(tank) for tank in tanks}

        return parameters

    def get_alerts(self, tank=None):
        '''Get any alerts (warning or critical) that may be lurking in our current parameters.'''
        result = dict(warnings={}, criticals={})

        tc = TankController()
        if not tank:
            tanks = [t.id for t in tc.get_tanks()]
        else:
            tanks = [tank]

        for tank in tanks:
            for param in tc.get_latest_parameters(tank):
                upper_limit = param.param.upper_limit
                lower_limit = param.param.lower_limit
                tolerance = param.param.tolerance
                value = param.value

                if value >= upper_limit:
                    msg = "{2} too high: {0}, but should be less than {1}".format(value, upper_limit - tolerance, param.param.name.title())
                    if value >= upper_limit - tolerance:
                        result['warnings'][param] = msg
                    else:
                        result['criticals'][param] = msg
                elif value <= lower_limit:
                    msg = "{2} too low: {0}, but should be more than {1}".format(value, lower_limit + tolerance, param.param.name.title())
                    if value <= lower_limit + tolerance:
                        result['warnings'][param] = msg
                    else:
                        result['criticals'][param] = msg

        return result
