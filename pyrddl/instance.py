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


from typing import Dict, List, Sequence, Tuple, Union

FluentTuple = Tuple[Union[str, None]]
Value = Union[bool, int, float]
FluentInitializer = Tuple[FluentTuple, Value]
FluentInitializerList = List[FluentInitializer]


class Instance(object):
    '''Instance class for accessing RDDL instance sections.

    Note:
        This class is intended to be solely used by the parser and compiler.
        Do not attempt to directly use this class to build an Instance object.

    Args:
        name: Name of RDDL instance.
        sections: Mapping from string to instance section.

    Attributes:
        name (str): Name of RDDL instance.
        domain (str): Name of RDDL domain.
        non_fluents (str): Name of RDDL non-fluents.
        init_state (:obj:`FluentInitializerList`): List of initial state initializers.
        max_nondef_actions (Union[int, str]): Maximum number of non-default actions.
        horizon (Union[int, str]): Number of decision timesteps.
        discount (float): Discount factor.
    '''

    def __init__(self, name: str, sections: Dict[str, Sequence]) -> None:
        self.name = name
        self.__dict__.update(sections)
