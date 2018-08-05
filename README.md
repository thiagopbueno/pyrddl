# pyrddl [![Build Status](https://travis-ci.org/thiagopbueno/pyrddl.svg?branch=master)](https://travis-ci.org/thiagopbueno/pyrddl) [![License](https://img.shields.io/aur/license/yaourt.svg)](https://github.com/thiagopbueno/tf-mdp/blob/master/LICENSE)

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
into your own Python package/project.

```python
from pyrddl import RDDLParser

# buid parser
parser = RDDLParser()
parser.build()

# parse RDDL
rddl = parser.parse(rddl)
```
