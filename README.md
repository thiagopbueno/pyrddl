# pyrddl [![Build Status](https://travis-ci.org/thiagopbueno/pyrddl.svg?branch=master)](https://travis-ci.org/thiagopbueno/pyrddl) [![License](https://img.shields.io/aur/license/yaourt.svg)](https://github.com/thiagopbueno/pyrddl/blob/master/LICENSE)

RDDL lexer/parser in Python3.

# Quickstart

```bash
$ pip3 install pyrddl
```

# Usage


## Script mode

The ``pyrddl`` script provides ways to parse and inspect RDDL files
from the command line.

```bash
$pyrddl --help

usage: pyrddl [-h] [-v] rddl

RDDL lexer/parser in Python3.

positional arguments:
  rddl           RDDL filepath

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  verbosity mode
```

## Programmatic mode

The ``pyrddl`` package provides an API for integrating RDDL parser
with your own Python package/project.

```python
from pyrddl import RDDLParser

# buid parser
parser = RDDLParser()
parser.build()

# parse RDDL
rddl = parser.parse(rddl)
```

# License

Copyright (c) 2018 Thiago Pereira Bueno All Rights Reserved.

pyrddl is free software: you can redistribute it and/or modify it
under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at
your option) any later version.

pyrddl is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with pyrddl. If not, see http://www.gnu.org/licenses/.
