#!/usr/bin/env python

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


from flask.ext.script import Manager

from autotriops.main import create_app
from autotriops.controllers import TankController, ParameterController

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
