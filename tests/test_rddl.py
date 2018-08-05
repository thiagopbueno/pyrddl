from pyrddl.parser import RDDLParser
from pyrddl.pvariable import PVariable

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
        cls.rddl2 = parser.parse(MARS_ROVER)
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
