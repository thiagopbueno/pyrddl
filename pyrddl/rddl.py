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


from pyrddl.domain import Domain
from pyrddl.instance import Instance
from pyrddl.nonfluents import NonFluents

from typing import Dict, Union

Block = Union[Domain, NonFluents, Instance]


class RDDL(object):
    '''RDDL class for accessing RDDL blocks.

    Note:
        This class is intended to be solely used by the parser and compiler.
        Do not attempt to directly use this class to build a RDDL object.

    Args:
        blocks: Mapping from string to RDDL block.

    Attributes:
        domain (:obj:`Domain`): RDDL domain block.
        non_fluents (:obj:`NonFluents`): RDDL non-fluents block.
        instance (:obj:`Instance`): RDDL instance block.
    '''

    def __init__(self, blocks: Dict[str, Block]) -> None:
        self.domain = blocks['domain']
        self.non_fluents = blocks['non_fluents']
        self.instance = blocks['instance']
