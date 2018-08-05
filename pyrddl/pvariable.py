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


from typing import List, Optional, Union

FluentValue = Union[bool, int, float]


class PVariable(object):
    '''Parameterized Variable.

    Note:
        This class is intended to be solely used by the parser and compiler.
        Do not attempt to directly use this class to build a PVariable object.

    Args:
        name (str): Name of fluent.
        fluent_type (str): Type of fluent.
        range (str): Range of fluent.
        param_types (Optional[List[str]]): List of parameter types.
        default (Optional[FluentValue]): Default value of fluent.
        level (Optional[int]): Level of intermediate fluent.

    Attributes:
        name (str): Name of fluent.
        fluent_type (str): Type of fluent.
        range (str): Range of fluent.
        param_types (Optional[List[str]]): List of parameter types.
        default (Optional[FluentValue]): Default value of fluent.
        level (Optional[int]): Level of intermediate fluent.
    '''

    def __init__(self,
            name: str,
            fluent_type: str,
            range_type: str,
            param_types: Optional[List[str]] = None,
            default: Optional[FluentValue] = None,
            level: Optional[int] = None) -> None:
        self.name = name
        self.fluent_type = fluent_type
        self.range = range_type
        self.param_types = param_types
        self.default = default
        self.level = level

    @property
    def arity(self) -> int:
        '''Returns arity of fluent.'''
        return len(self.param_types) if self.param_types is not None else 0

    def is_non_fluent(self) -> bool:
        '''Returns True if fluent is of non-fluent type. False, otherwise.'''
        return self.fluent_type == 'non-fluent'

    def is_state_fluent(self) -> bool:
        '''Returns True if fluent is of state-fluent type. False, otherwise.'''
        return self.fluent_type == 'state-fluent'

    def is_action_fluent(self) -> bool:
        '''Returns True if fluent is of action-fluent type. False, otherwise.'''
        return self.fluent_type == 'action-fluent'

    def is_intermediate_fluent(self) -> bool:
        '''Returns True if fluent is of interm-fluent type. False, otherwise.'''
        return self.fluent_type == 'interm-fluent'

    def __str__(self) -> str:
        '''Returns string value of PVariable.'''
        return '{}/{}'.format(self.name, self.arity)

    def __repr__(self) -> str:
        '''Returns canonical string representation of PVariable.'''
        return self.name if self.arity == 0 else '{}({})'.format(self.name, ','.join(self.param_types))
