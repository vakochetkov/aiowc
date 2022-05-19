import os
import sys

from setuptools import setup


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# check python version
MINIMAL_PY_VERSION = (3, 7)
if sys.version_info < MINIMAL_PY_VERSION:
    raise RuntimeError('aiowc works only with Python {}+'.format('.'.join(map(str, MINIMAL_PY_VERSION))))

if __name__ == '__main__':
    setup()
