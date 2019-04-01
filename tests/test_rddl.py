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

    def test_state_fluent_variables(self):
        rddls = [self.rddl1, self.rddl2]
        fluent_variables = [
            {
            'rlevel/1': ['rlevel(t1)', 'rlevel(t2)', 'rlevel(t3)', 'rlevel(t4)', 'rlevel(t5)', 'rlevel(t6)', 'rlevel(t7)', 'rlevel(t8)']
            },
            {
                'picTaken/1': ['picTaken(p1)', 'picTaken(p2)', 'picTaken(p3)'],
                'time/0': ['time'],
                'xPos/0': ['xPos'],
                'yPos/0': ['yPos']
            }
        ]
        for rddl, expected_variables in zip(rddls, fluent_variables):
            fluent_variables = rddl.state_fluent_variables
            self.assertEqual(len(fluent_variables), len(expected_variables))
            for name, actual_variables in fluent_variables:
                self.assertIn(name, expected_variables)
                self.assertListEqual(actual_variables, expected_variables[name])

    def test_interm_fluent_variables(self):
        rddls = [self.rddl1, self.rddl2]
        fluent_variables = [
            {
            'evaporated/1': ['evaporated(t1)', 'evaporated(t2)', 'evaporated(t3)', 'evaporated(t4)', 'evaporated(t5)', 'evaporated(t6)', 'evaporated(t7)', 'evaporated(t8)'],
            'rainfall/1': ['rainfall(t1)', 'rainfall(t2)', 'rainfall(t3)', 'rainfall(t4)', 'rainfall(t5)', 'rainfall(t6)', 'rainfall(t7)', 'rainfall(t8)'],
            'overflow/1': ['overflow(t1)', 'overflow(t2)', 'overflow(t3)', 'overflow(t4)', 'overflow(t5)', 'overflow(t6)', 'overflow(t7)', 'overflow(t8)'],
            'inflow/1': ['inflow(t1)', 'inflow(t2)', 'inflow(t3)', 'inflow(t4)', 'inflow(t5)', 'inflow(t6)', 'inflow(t7)', 'inflow(t8)']
            },
            {}
        ]
        for rddl, expected_variables in zip(rddls, fluent_variables):
            fluent_variables = rddl.interm_fluent_variables
            self.assertEqual(len(fluent_variables), len(expected_variables))
            for name, actual_variables in fluent_variables:
                self.assertIn(name, expected_variables)
                self.assertListEqual(actual_variables, expected_variables[name])

    def test_action_fluent_variables(self):
        rddls = [self.rddl1, self.rddl2]
        fluent_variables = [
            {
                'outflow/1': ['outflow(t1)', 'outflow(t2)', 'outflow(t3)', 'outflow(t4)', 'outflow(t5)', 'outflow(t6)', 'outflow(t7)', 'outflow(t8)']
            },
            {
                'snapPicture/0': ['snapPicture'],
                'xMove/0': ['xMove'],
                'yMove/0': ['yMove']
            }
        ]
        for rddl, expected_variables in zip(rddls, fluent_variables):
            fluent_variables = rddl.action_fluent_variables
            self.assertEqual(len(fluent_variables), len(expected_variables))
            for name, actual_variables in fluent_variables:
                self.assertIn(name, expected_variables)
                self.assertListEqual(actual_variables, expected_variables[name])
