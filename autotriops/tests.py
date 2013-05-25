
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

from flask.ext.testing import TestCase

from db import db
from controllers import TankController

class TestTankController(TestCase):

    def create_app(self):
        from main import create_app
        return create_app()

    def setUp(self):
        db.create_all()

        self.tc = TankController()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_tank(self):
        result = self.tc.add_tank("10gal")
        assert result

    def test_update_parameter(self):
        tank = self.tc.add_tank("10gal")
        result = self.tc.update_parameter(tank.id, "asf", 32)
        assert result

    def test_get_latest_parameters(self):
        tank = self.tc.add_tank("10gal")
        self.tc.update_parameter(tank.id, "asf", 32)
        self.tc.update_parameter(tank.id, "asf", 42)
        self.tc.update_parameter(tank.id, "asf", 52)
        result = self.tc.get_latest_parameters(tank.id)
        assert result
        assert len(result) == 1
        assert result[0].value == 52
