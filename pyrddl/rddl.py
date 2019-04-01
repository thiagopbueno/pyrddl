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

from typing import Dict, List, Union

Block = Union[Domain, NonFluents, Instance]
ObjectStruct = Dict[str, Union[int, Dict[str, int], List[str]]]
ObjectTable = Dict[str, ObjectStruct]


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
        object_table (:obj:`ObjectTable`): The object table for each RDDL type.
    '''

    def __init__(self, blocks: Dict[str, Block]) -> None:
        self.domain = blocks['domain']
        self.non_fluents = blocks['non_fluents']
        self.instance = blocks['instance']

    def build(self):
        self.domain.build()
        self._build_object_table()

    def _build_object_table(self):
        '''Builds the object table for each RDDL type.'''
        types = self.domain.types
        objects = dict(self.non_fluents.objects)
        self.object_table = dict()
        for name, value in self.domain.types:
            if value == 'object':
                objs = objects[name]
                idx = { obj: i for i, obj in enumerate(objs) }
                self.object_table[name] = {
                    'size': len(objs),
                    'idx': idx,
                    'objects': objs
                }
