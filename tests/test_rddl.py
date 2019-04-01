# This file is part of pyrddl.

# pyrddl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pyrddl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with pyrddl. If not, see <http://www.gnu.org/licenses/>.


from pyrddl.parser import RDDLParser

import unittest


class TestRDDL(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open('rddl/Reservoir.rddl', mode='r') as file:
            RESERVOIR = file.read()

        with open('rddl/Mars_Rover.rddl', mode='r') as file:
            MARS_ROVER = file.read()

        parser = RDDLParser()
        parser.build()

        cls.rddl1 = parser.parse(RESERVOIR)
        cls.rddl1.build()
        cls.rddl2 = parser.parse(MARS_ROVER)
        cls.rddl2.build()
        cls.rddls = [cls.rddl1, cls.rddl2]

    def test_build_object_table(self):
        self.assertIn('res', self.rddl1.object_table)
        size = self.rddl1.object_table['res']['size']
        idx = self.rddl1.object_table['res']['idx']
        self.assertEqual(size, 8)
        objs = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8']
        for i, obj in enumerate(objs):
            self.assertIn(obj, idx)
            self.assertEqual(idx[obj], i)
