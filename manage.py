#!/usr/bin/env python

from flask.ext.script import Manager

from main import create_app
from controllers import TankController, ParameterController

manager = Manager(create_app())

@manager.command
def add_tank(name):
    '''Add a tank with a given name.'''
    tc = TankController()
    print "Added tank:", tc.add_tank(name)

@manager.command
def add_param(name, upper_bound, lower_bound, tolerance):
    pc = ParameterController()
    print "Added a parameter:", pc.add_param(name, upper_bound, lower_bound, tolerance)

@manager.command
def update_param(tank, name, value):
    tc = TankController()
    tank = [t for t in tc.get_tanks() if t.name == tank][0].id
    result = tc.update_parameter(tank, name, value)
    if result:
        print "Updated parameter {0} for tank {1} to {2}".format(name, tank, value)

if __name__ == "__main__":
    manager.run()
