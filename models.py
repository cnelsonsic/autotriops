
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

from datetime import datetime

from db import db

class Parameter(db.Model):
    '''These are specific metrics that represent tank parameters like pH, water level, nitrates, etc.'''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

    # Warnings
    upper_limit = db.Column(db.Float)
    lower_limit = db.Column(db.Float)
    tolerance = db.Column(db.Float)

    def __init__(self, name, upper_limit, lower_limit, tolerance):
        self.name = name
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit
        self.tolerance = tolerance

    def __repr__(self):
        return "<Parameter name={self.name}, upper_limit={self.upper_limit}, lower_limit={self.lower_limit}, tolerance={self.tolerance}>".format(self=self)

class TankParameter(db.Model):
    '''These are specific instances of metrics.
    Example: Tank 1 had a pH of 7.1 yesterday, and a pH of 7.0 today.'''
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    value = db.Column(db.Float)

    tank_id = db.Column(db.Integer, db.ForeignKey('tank.id'))
    tank = db.relationship('Tank', backref=db.backref('tankparameter', lazy='dynamic'))

    param_id = db.Column(db.Integer, db.ForeignKey('parameter.id'))
    param = db.relationship('Parameter', backref=db.backref('tankparameter', lazy='dynamic'))

    def __init__(self, param, value, tank, timestamp=None):
        self.value = value
        self.tank = tank
        self.param = param

        if not timestamp:
            self.timestamp = datetime.utcnow()

class Tank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Tank id={self.id}, name={self.name}>".format(self=self)
