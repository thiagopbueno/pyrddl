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


from pyrddl import utils
from pyrddl.pvariable import PVariable
from pyrddl.cpf import CPF
from pyrddl.expr import Expression


from typing import Dict, List, Sequence, Tuple

Type = Tuple[str, str]


class Domain(object):
    '''Domain class for accessing RDDL domain sections.

    Note:
        This class is intended to be solely used by the parser and compiler.
        Do not attempt to directly use this class to build a Domain object.

    Args:
        name: Name of RDDL domain.
        requirements: List of RDDL requirements.
        sections: Mapping from string to domain section.

    Attributes:
        name (str): Domain identifier.
        requirements (List[str]): List of requirements.
        types (List[:obj:`Type`]): List of types.
        pvariables (List[:obj:`PVariable`]): List of parameterized variables.
        cpfs (List[:obj:`CPF`]): List of Conditional Probability Functions.
        reward (:obj:`Expression`): Reward function.
        preconds (List[:obj:`Expression`]): List of action preconditions.
        constraints (List[:obj:`Expression`]): List of state-action constraints.
        invariants (List[:obj:`Expression`]): List of state invariants.
    '''

    def __init__(self, name: str, requirements: List[str], sections: Dict[str, Sequence]) -> None:
        self.name = name
        self.requirements = requirements

        self.pvariables = sections['pvariables']
        self.cpfs = sections['cpfs']
        self.reward = sections['reward']

        self.types = sections.get('types', [])
        self.preconds = sections.get('preconds', [])
        self.invariants = sections.get('invariants', [])
        self.constraints = sections.get('constraints', [])

    @property
    def non_fluents(self) -> Dict[str, PVariable]:
        '''Returns non-fluent pvariables.'''
        return { str(pvar): pvar for pvar in self.pvariables if pvar.is_non_fluent() }

    @property
    def state_fluents(self) -> Dict[str, PVariable]:
        '''Returns state-fluent pvariables.'''
        return { str(pvar): pvar for pvar in self.pvariables if pvar.is_state_fluent() }

    @property
    def action_fluents(self) -> Dict[str, PVariable]:
        '''Returns action-fluent pvariables.'''
        return { str(pvar): pvar for pvar in self.pvariables if pvar.is_action_fluent() }

    @property
    def intermediate_fluents(self) -> Dict[str, PVariable]:
        '''Returns interm-fluent pvariables.'''
        return { str(pvar): pvar for pvar in self.pvariables if pvar.is_intermediate_fluent() }

    @property
    def intermediate_cpfs(self) -> List[CPF]:
        '''Returns list of intermediate-fluent CPFs in level order.'''
        _, cpfs = self.cpfs
        interm_cpfs = [cpf for cpf in cpfs if cpf.name in self.intermediate_fluents]
        interm_cpfs = sorted(interm_cpfs, key=lambda cpf: (self.intermediate_fluents[cpf.name].level, cpf.name))
        return interm_cpfs

    @property
    def state_cpfs(self) -> List[CPF]:
        '''Returns list of state-fluent CPFs.'''
        _, cpfs = self.cpfs
        state_cpfs = []
        for cpf in cpfs:
            name = utils.rename_next_state_fluent(cpf.name)
            if name in self.state_fluents:
                state_cpfs.append(cpf)
        state_cpfs = sorted(state_cpfs, key=lambda cpf: cpf.name)
        return state_cpfs
