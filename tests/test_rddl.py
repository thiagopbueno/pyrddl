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
from pyrddl.pvariable import PVariable

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

    def test_build_fluent_table(self):
        self.assertEqual(len(self.rddl1.fluent_table), 16)
        for name, (fluent, size) in self.rddl1.fluent_table.items():
            self.assertIsInstance(name, str)
            self.assertIn(fluent.name, name)
            self.assertIsInstance(fluent, PVariable)
            self.assertIsInstance(size, tuple)
            self.assertEqual(len(size), fluent.arity)

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

    def test_state_size(self):
        rddls = [self.rddl1, self.rddl2]
        for i, rddl in enumerate(rddls):
            state_size = rddl.state_size
            self.assertIsInstance(state_size, tuple)
            for shape in state_size:
                self.assertIsInstance(shape, tuple)

            state_fluent_ordering = rddl.domain.state_fluent_ordering
            next_state_fluent_ordering = rddl.domain.next_state_fluent_ordering
            self.assertEqual(len(state_size), len(state_fluent_ordering))
            self.assertEqual(len(state_size), len(next_state_fluent_ordering))

    def test_action_size(self):
        rddls = [self.rddl1, self.rddl2]
        for rddl in rddls:
            action_size = rddl.action_size
            action_fluent_ordering = rddl.domain.action_fluent_ordering
            self.assertIsInstance(action_size, tuple)
            self.assertEqual(len(action_size), len(action_fluent_ordering))
            for shape in action_size:
                self.assertIsInstance(shape, tuple)

    def test_interm_size(self):
        rddls = [self.rddl1, self.rddl2]
        for rddl in rddls:
            interm_size = rddl.interm_size
            interm_ordering = rddl.domain.interm_fluent_ordering
            self.assertIsInstance(interm_size, tuple)
            self.assertEqual(len(interm_size), len(interm_ordering))
            for shape in interm_size:
                self.assertIsInstance(shape, tuple)

    def test_state_range_type(self):
        rddls = [self.rddl1, self.rddl2]
        for rddl in rddls:
            state_range_type = rddl.state_range_type
            state_fluents = rddl.domain.state_fluents
            state_fluent_ordering = rddl.domain.state_fluent_ordering
            self.assertIsInstance(state_range_type, tuple)
            self.assertEqual(len(state_range_type), len(state_fluents))
            self.assertEqual(len(state_range_type), len(state_fluent_ordering))
            for name, range_type in zip(state_fluent_ordering, state_range_type):
                fluent = state_fluents[name]
                self.assertIsInstance(range_type, str)
                self.assertEqual(range_type, fluent.range)

    def test_interm_range_type(self):
        rddls = [self.rddl1, self.rddl2]
        for rddl in rddls:
            interm_range_type = rddl.interm_range_type
            interm_fluents = rddl.domain.intermediate_fluents
            interm_fluent_ordering = rddl.domain.interm_fluent_ordering
            self.assertIsInstance(interm_range_type, tuple)
            self.assertEqual(len(interm_range_type), len(interm_fluents))
            self.assertEqual(len(interm_range_type), len(interm_fluent_ordering))
            for name, range_type in zip(interm_fluent_ordering, interm_range_type):
                fluent = interm_fluents[name]
                self.assertIsInstance(range_type, str)
                self.assertEqual(range_type, fluent.range)

    def test_action_range_type(self):
        rddls = [self.rddl1, self.rddl2]
        for rddl in rddls:
            action_range_type = rddl.action_range_type
            action_fluents = rddl.domain.action_fluents
            action_fluent_ordering = rddl.domain.action_fluent_ordering
            self.assertIsInstance(action_range_type, tuple)
            self.assertEqual(len(action_range_type), len(action_fluents))
            self.assertEqual(len(action_range_type), len(action_fluent_ordering))
            for name, range_type in zip(action_fluent_ordering, action_range_type):
                fluent = action_fluents[name]
                self.assertIsInstance(range_type, str)
                self.assertEqual(range_type, fluent.range)
