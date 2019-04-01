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
from pyrddl.expr import Expression
from pyrddl import utils

import unittest


class TestDomain(unittest.TestCase):

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

    def test_non_fluents(self):
        expected_non_fluents = [
            {
                'MAX_RES_CAP/1',
                'UPPER_BOUND/1',
                'LOWER_BOUND/1',
                'RAIN_SHAPE/1',
                'RAIN_SCALE/1',
                'DOWNSTREAM/2',
                'SINK_RES/1',
                'MAX_WATER_EVAP_FRAC_PER_TIME_UNIT/0',
                'LOW_PENALTY/1',
                'HIGH_PENALTY/1'
            },
            {
                'MAX_TIME/0',
                'MOVE_VARIANCE_MULT/0',
                'PICT_XPOS/1',
                'PICT_YPOS/1',
                'PICT_VALUE/1',
                'PICT_ERROR_ALLOW/1'
            }
        ]

        for rddl, expected in zip(self.rddls, expected_non_fluents):
            fluents = rddl.domain.non_fluents
            self.assertEqual(len(fluents), len(expected))
            for name in expected:
                self.assertIn(name, fluents)
                pvar = fluents[name]
                self.assertIsInstance(pvar, PVariable)
                self.assertTrue(pvar.is_non_fluent())

    def test_state_fluents(self):
        expected_state_fluents = [
            {
                'rlevel/1'
            },
            {
                'xPos/0',
                'yPos/0',
                'time/0',
                'picTaken/1'
            }
        ]
        for rddl, expected in zip(self.rddls, expected_state_fluents):
            fluents = rddl.domain.state_fluents
            self.assertEqual(len(fluents), len(expected))
            for name in expected:
                self.assertIn(name, fluents)
                pvar = fluents[name]
                self.assertIsInstance(pvar, PVariable)
                self.assertTrue(pvar.is_state_fluent())

    def test_action_fluents(self):
        expected_action_fluents = [
            {
                'outflow/1'
            },
            {
                'xMove/0',
                'yMove/0',
                'snapPicture/0'
            }
        ]
        for rddl, expected in zip(self.rddls, expected_action_fluents):
            fluents = rddl.domain.action_fluents
            self.assertEqual(len(fluents), len(expected))
            for name in expected:
                self.assertIn(name, fluents)
                pvar = fluents[name]
                self.assertIsInstance(pvar, PVariable)
                self.assertTrue(pvar.is_action_fluent())

    def test_intermediate_fluents(self):
        expected_intermediate_fluents = [
            {
                'evaporated/1',
                'rainfall/1',
                'overflow/1',
                'inflow/1'
            },
            {}
        ]
        for rddl, expected in zip(self.rddls, expected_intermediate_fluents):
            fluents = rddl.domain.intermediate_fluents
            self.assertEqual(len(fluents), len(expected))
            for name in expected:
                self.assertIn(name, fluents)
                pvar = fluents[name]
                self.assertIsInstance(pvar, PVariable)
                self.assertTrue(pvar.is_intermediate_fluent())

    def test_intermediate_cpfs(self):
        rddls = [self.rddl1, self.rddl2]
        for rddl in rddls:
            interm_cpfs = rddl.domain.intermediate_cpfs
            self.assertIsInstance(interm_cpfs, list)

            interm_fluents = rddl.domain.intermediate_fluents
            self.assertEqual(len(interm_cpfs), len(interm_fluents))
            for cpf in interm_cpfs:
                self.assertIn(cpf.name, interm_fluents)

            for i, cpf in enumerate(interm_cpfs[:-1]):
                level1 = interm_fluents[cpf.name].level
                level2 = interm_fluents[interm_cpfs[i+1].name].level
                self.assertLessEqual(level1, level2)

    def test_state_cpfs(self):
        rddls = [self.rddl1, self.rddl2]
        for rddl in rddls:
            state_cpfs = rddl.domain.state_cpfs
            self.assertIsInstance(state_cpfs, list)

            state_fluents = rddl.domain.state_fluents
            self.assertEqual(len(state_cpfs), len(state_fluents))
            for cpf in state_cpfs:
                name = cpf.name
                functor = name[:name.index('/')-1]
                arity = name[name.index('/')+1:]
                name = '{}/{}'.format(functor, arity)
                self.assertIn(name, state_fluents)

    def test_non_fluent_ordering(self):
        rddls = [self.rddl1, self.rddl2]
        for rddl in rddls:
            non_fluents = rddl.domain.non_fluents
            non_fluent_ordering = rddl.domain.non_fluent_ordering
            self.assertIsInstance(non_fluent_ordering, list)
            self.assertEqual(len(non_fluent_ordering), len(non_fluents))
            for non_fluent in non_fluent_ordering:
                self.assertIn(non_fluent, non_fluents)
            self.assertListEqual(non_fluent_ordering, sorted(non_fluent_ordering))

    def test_state_fluent_ordering(self):
        rddls = [self.rddl1, self.rddl2]
        for rddl in rddls:
            current_state_fluents = rddl.domain.state_fluents
            current_state_ordering = rddl.domain.state_fluent_ordering
            self.assertIsInstance(current_state_ordering, list)
            self.assertEqual(len(current_state_ordering), len(current_state_fluents))
            for fluent in current_state_fluents:
                self.assertIn(fluent, current_state_ordering)
            self.assertListEqual(current_state_ordering, sorted(current_state_ordering))

            next_state_ordering = rddl.domain.next_state_fluent_ordering
            self.assertIsInstance(next_state_ordering, list)

            self.assertEqual(len(current_state_ordering), len(next_state_ordering))
            for current_fluent, next_fluent in zip(current_state_ordering, next_state_ordering):
                self.assertEqual(utils.rename_state_fluent(current_fluent), next_fluent)
                self.assertEqual(utils.rename_next_state_fluent(next_fluent), current_fluent)

    def test_action_fluent_ordering(self):
        rddls = [self.rddl1, self.rddl2]
        for rddl in rddls:
            action_fluents = rddl.domain.action_fluents
            action_fluent_ordering = rddl.domain.action_fluent_ordering
            self.assertIsInstance(action_fluent_ordering, list)
            self.assertEqual(len(action_fluent_ordering), len(action_fluents))
            for action_fluent in action_fluent_ordering:
                self.assertIn(action_fluent, action_fluents)
            self.assertListEqual(action_fluent_ordering, sorted(action_fluent_ordering))

    def test_interm_fluent_ordering(self):
        rddls = [self.rddl1, self.rddl2]
        for rddl in rddls:
            interm_fluents = rddl.domain.intermediate_fluents
            interm_fluent_ordering = rddl.domain.interm_fluent_ordering
            self.assertIsInstance(interm_fluent_ordering, list)
            self.assertEqual(len(interm_fluent_ordering), len(interm_fluents))
            for interm_fluent in interm_fluent_ordering:
                self.assertIn(interm_fluent, interm_fluents)

            for i in range(1, len(interm_fluent_ordering) - 1):
                name1, name2 = interm_fluent_ordering[i], interm_fluent_ordering[i+1]
                fluent1, fluent2 = interm_fluents[name1], interm_fluents[name2]
                self.assertLessEqual(fluent1.level, fluent2.level)
                if fluent1.level == fluent2.level:
                    self.assertLessEqual(fluent1.name, fluent2.name)

    def test_build_action_preconditions_table(self):
        local_preconds = self.rddl1.domain.local_action_preconditions
        self.assertIsInstance(local_preconds, dict)
        self.assertEqual(len(local_preconds), 1)
        self.assertIn('outflow/1', local_preconds)
        self.assertEqual(len(local_preconds['outflow/1']), 2)

        global_preconds = self.rddl1.domain.global_action_preconditions
        self.assertIsInstance(global_preconds, list)
        self.assertEqual(len(global_preconds), 0)

    def test_lower_bound_constraints(self):
        lower_bounds = self.rddl1.domain.action_lower_bound_constraints
        self.assertIsInstance(lower_bounds, dict)
        self.assertIn('outflow/1', lower_bounds)
        lower = lower_bounds['outflow/1']
        self.assertIsInstance(lower, Expression)
        self.assertTrue(lower.is_constant_expression())
        self.assertEqual(lower.value, 0)

        # lower_bounds = self.rddl3.action_lower_bound_constraints
        # self.assertIsInstance(lower_bounds, dict)
        # self.assertIn('AIR/1', lower_bounds)
        # lower = lower_bounds['AIR/1']
        # self.assertIsInstance(lower, Expression)
        # self.assertTrue(lower.is_constant_expression())
        # self.assertEqual(lower.value, 0)

    def test_upper_bound_constraints(self):
        upper_bounds = self.rddl1.domain.action_upper_bound_constraints
        self.assertIsInstance(upper_bounds, dict)
        self.assertIn('outflow/1', upper_bounds)
        upper = upper_bounds['outflow/1']
        self.assertIsInstance(upper, Expression)
        self.assertTrue(upper.is_pvariable_expression())
        self.assertEqual(upper.name, 'rlevel/1')
