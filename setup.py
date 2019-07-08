"""

everycompare :  Copyright 2018-2019, Michal Wozniczak

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

see: https://www.gnu.org/licenses/#GPL

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
contained in the program LICENSE file.

"""

import os
import sys
import platform
import subprocess
from shutil import which
from shutil import copy2 as copyfile
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
import getpass
from pathlib import Path
from codecs import open
import everycompare


requires = [
    'binaryornot',
    'tqdm>=4.32.0',
    'python-levenshtein-wheels'
]


_project = 'everycompare'
_root = os.path.abspath(os.path.dirname(__file__))


def _root_user():
    """
    Checks localhost root or sudo access.  Returns bool
    """
    if os.geteuid() == 0:
        return True
    elif subprocess.getoutput('echo $EUID') == '0':
        return True
    return False


def os_parityPath(path):
    """
    Converts unix paths to correct windows equivalents.
    Unix native paths remain unchanged (no effect)
    """
    path = os.path.normpath(os.path.expanduser(path))
    if path.startswith('\\'):
        return 'C:' + path
    return path


class PostInstallDevelop(develop):
    """ post-install, development """
    def run(self):
        subprocess.check_call("bash scripts/post-install-dev.sh".split())
        develop.run(self)


def preclean(dst):
    if os.path.exists(dst):
        os.remove(dst)
    return True


def read(fname):
    basedir = os.path.dirname(sys.argv[0])
    return open(os.path.join(basedir, fname)).read()


def sourcefile_content():
    sourcefile = """
    for bcfile in ~/.bash_completion.d/* ; do
        [ -f "$bcfile" ] && . $bcfile
    done\n
    """
    return sourcefile


setup(
    name=_project,
    version=everycompare.__version__,
    description='Count the number of lines of code in a project',
    long_description=read('DESCRIPTION.rst'),
    url='https://github.com/fstab50/everycompare',
    author=everycompare.__author__,
    author_email=everycompare.__email__,
    license='GPL-3.0',
    classifiers=[
        'Topic :: Software Development :: Build Tools',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows'
    ],
    keywords='code development tools',
    packages=find_packages(exclude=['assets', 'docs', 'reports', 'scripts', 'tests']),
    include_package_data=True,
    install_requires=requires,
    python_requires='>=3.6, <4',
    entry_points={
        'console_scripts': [
            'everycompare=everycompare.cli:main'
        ]
    },
    zip_safe=False
)
