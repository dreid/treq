#!/usr/bin/env python

from __future__ import absolute_import, print_function

import re
import sys


travis_template = """\
# AUTO-GENERATED BY tox2travis.py -- DO NOT EDIT THIS FILE BY HAND!

sudo: false
language: python

cache: false

matrix:
  include:
    {includes}

  # Don't fail on trunk versions.
  allow_failures:
    - env: TOX_ENV=pypy-twisted_trunk-pyopenssl_trunk
    - env: TOX_ENV=py27-twisted_trunk-pyopenssl_trunk
    - env: TOX_ENV=py33-twisted_trunk-pyopenssl_trunk
    - env: TOX_ENV=py34-twisted_trunk-pyopenssl_trunk
    - env: TOX_ENV=py35-twisted_trunk-pyopenssl_trunk

before_install:
  - |
    if [[ "${{TOX_ENV::5}}" == "pypy-" ]]; then
      PYENV_ROOT="$HOME/.pyenv"
      git clone --depth 1 https://github.com/yyuu/pyenv.git "$PYENV_ROOT"
      PATH="$PYENV_ROOT/bin:$PATH"
      eval "$(pyenv init -)"
      pyenv install pypy-5.4.1
      pyenv global pypy-5.4.1
    fi

install:
  - pip install tox codecov

script:
  - tox -e $TOX_ENV

after_success:
  - codecov

notifications:
  email: false

branches:
  only:
    - master

# AUTO-GENERATED BY tox2travis.py -- DO NOT EDIT THIS FILE BY HAND!"""


if __name__ == "__main__":
    line = sys.stdin.readline()
    tox_envs = []
    while line:
        tox_envs.append(line.strip())
        line = sys.stdin.readline()

    includes = []
    for tox_env in tox_envs:
        # Parse the Python version from the tox environment name
        python_match = re.match(r'^py(?:(\d{2})|py)-', tox_env)
        if python_match is not None:
            version = python_match.group(1)
            if version is not None:
                python = "'{0}.{1}'".format(version[0], version[1])
            else:
                python = 'pypy'
        else:
            python = "'2.7'"  # Default to Python 2.7 if a version isn't found

        includes.extend([
            '- python: {0}'.format(python),
            '  env: TOX_ENV={0}'.format(tox_env)
        ])

    print(travis_template.format(includes='\n    '.join(includes)))
