# This file is part of tf-rddlsim.

# tf-rddlsim is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# tf-rddlsim is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with tf-rddlsim. If not, see <http://www.gnu.org/licenses/>.


def rename_next_state_fluent(name: str) -> str:
    '''Returns next state fluent canonical name.

    Args:
        name (str): The current state fluent name.

    Returns:
        str: The next state fluent name.
    '''
    i = name.index('/')
    functor = name[:i-1]
    arity = name[i+1:]
    return "{}/{}".format(functor, arity)


def rename_state_fluent(name: str) -> str:
    '''Returns current state fluent canonical name.

    Args:
        name (str): The next state fluent name.

    Returns:
        str: The current state fluent name.
    '''
    i = name.index('/')
    functor = name[:i]
    arity = name[i+1:]
    return "{}'/{}".format(functor, arity)
