import pyrddl

import os
from setuptools import setup, find_packages


def read(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    file = open(filepath, 'r')
    return file.read()


setup(
    name='pyrddl',
    version=pyrddl.__version__,
    author='Thiago P. Bueno',
    author_email='thiago.pbueno@gmail.com',
    description='RDDL lexer/parser in Python3.',
    long_description=read('README.md'),
    license='GNU General Public License v3.0',
    keywords=['rddl', 'parser', 'mdp', 'dbn'],
    url='https://github.com/thiagopbueno/pyrddl',
    packages=find_packages(),
    scripts=['scripts/pyrddl'],
    install_requires=[
        'ply',
        'typing'
    ],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ],
)