#!/usr/bin/env python
# Sourdough
#
# Copyright 2017-2018 Joe Block <jpb@unixorn.net>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
setup.py for sourdough
'''

import os
import shutil
import subprocess
from setuptools import setup, find_packages, Command

def system_call(command):
    '''
    Run a command and return stdout.

    Would be better to use subprocess.check_output, but this works on 2.6,
    which is still the system Python on CentOS 7.
    '''
    procs = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    return procs.stdout.read()


NAME = 'sourdough'
VERSION = '1.0.2'

class CleanCommand(Command):
    '''
    Add a clean option to setup.py's commands
    '''
    description = 'Clean up'
    user_options = []


    def initialize_options(self):
        """
        Initialize Options
        """
        self.cwd = None


    def finalize_options(self):
        """
        finalize options
        """
        self.cwd = os.getcwd()

    def run(self):
        """
        Run
        """
        assert os.getcwd() == self.cwd, "Must be in package root: %s" % self.cwd
        if os.path.isdir('build'):
            shutil.rmtree('build')
        if os.path.isdir('dist'):
            shutil.rmtree('dist')


setup(
    name=NAME,
    author="Joe Block",
    author_email="jpb@unixorn.net",
    description="sourdough is a tool to make an instance automatically register with Chef during boot",
    url="https://github.com/unixorn/sourdough",
    packages=find_packages(),
    install_requires=[
        "boto>=2.38.0",
        "haze>=0.0.13",
        "logrus>=0.0.2",
        "pytoml>=0.1.11",
        "pyvim>=2.0.24",
        "pyvmomi>=6.7.1.2018.12",
        "six>=1.12.0"
    ],
    cmdclass={
        "clean": CleanCommand,
    },
    version=VERSION,
    download_url="https://github.com/unixorn/sourdough/tarball/%s" % VERSION,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: POSIX",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 2.6",
        "Topic :: System :: Systems Administration",
    ],
    keywords=['aws', 'chef', 'cloud', 'configuration-management', 'ec2'],
    entry_points={
        "console_scripts": [
            "sourdough = %s.cli.commands:sourdoughDriver" % NAME,
            "sourdough-bootstrap = %s.sourdough:infect" % NAME,
            "sourdough-deregister = %s.sourdough:deregisterFromChef" % NAME,
            "sourdough-disable-chef = %s.sourdough:disableChefRuns" % NAME,
            "sourdough-enable-chef = %s.sourdough:enableChefRuns" % NAME,
            "sourdough-disable-debugging = %s.sourdough:disableDebugMode" % NAME,
            "sourdough-enable-debugging = %s.sourdough:enableDebugMode" % NAME,
            "sourdough-runner = %s.sourdough:runner" % NAME,
            "sourdough-starter = %s.sourdough:runner" % NAME
        ]
    }
)
