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


import pytest

import rddlgym

from pyrddl.expr import Expression
from pyrddl.rddl import RDDL


@pytest.fixture(scope='module', params=['Reservoir-8', 'HVAC-3', 'Navigation-v3'])
def rddl(request):
    yield rddlgym.make(request.param, mode=rddlgym.AST)


def test_build_object_table(rddl):
    assert rddl.object_table is not None


def test_build_fluent_table(rddl):
    assert rddl.fluent_table is not None


def test_get_dependencies(rddl):

    if rddl.domain.name == 'reservoir':
        shape = Expression(('pvar_expr', ('RAIN_SHAPE', ['?res'])))
        scale = Expression(('pvar_expr', ('RAIN_SCALE', ['?res'])))
        gamma = Expression(('randomvar', ('Gamma', (shape, scale))))

        deps = rddl.get_dependencies(gamma)
        assert isinstance(deps, set)
        assert len(deps) == 2
        deps = set(map(lambda fluent: str(fluent), deps))
        assert deps == {'RAIN_SCALE/1', 'RAIN_SHAPE/1'}

    elif rddl.domain.name == 'hvac_vav_fix':
        mean = Expression(('pvar_expr', ('TEMP_OUTSIDE_MEAN', ['?s'])))
        variance = Expression(('pvar_expr', ('TEMP_OUTSIDE_VARIANCE', ['?s'])))
        normal = Expression(('randomvar', ('Normal', (mean, variance))))

        deps = rddl.get_dependencies(normal)
        assert isinstance(deps, set)
        assert len(deps) == 2
        deps = set(map(lambda fluent: str(fluent), deps))
        assert deps == {'TEMP_OUTSIDE_MEAN/1', 'TEMP_OUTSIDE_VARIANCE/1'}

    elif rddl.domain.name == 'Navigation':
        location = Expression(('pvar_expr', ('location', ['?l'])))
        move = Expression(('pvar_expr', ('move', ['?l'])))
        deceleration = Expression(
            ('prod', (
                ('typed_var', ('?z', 'zone')),
                Expression(('pvar_expr', ('deceleration', ['?z']))))))

        mean = Expression(('+', (location, Expression(('*', (deceleration, move))))))
        variance = Expression(('*',
                        (Expression(('pvar_expr', ('MOVE_VARIANCE_MULT', ['?l']))), move)))
        normal = Expression(('randomvar', ('Normal', (mean, variance))))

        deps = rddl.get_dependencies(normal)
        assert isinstance(deps, set)
        assert len(deps) == 5
        deps = set(map(lambda fluent: str(fluent), deps))
        assert deps == {
            'location/1', 'move/1',
            'DECELERATION_ZONE_CENTER/2', 'DECELERATION_ZONE_DECAY/1',
            'MOVE_VARIANCE_MULT/1'
        }
