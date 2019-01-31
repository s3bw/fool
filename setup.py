import os
from codecs import open

from setuptools import setup
from setuptools import find_packages


HERE = os.path.abspath(os.path.dirname(__file__))
PATH_VERSION = os.path.join(HERE, 'fool', '__version__.py')


about = {}
with open(PATH_VERSION, 'r', 'utf-8') as f:
    exec(f.read(), about)


setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    author='s.williamswynn.mail@gmail.com',
    packages=find_packages(
        include=[
            'fool',
            'fool.*',
        ],
    ),
    install_requires=[
        'pytest==4.2.0',
    ],
    setup_requires=[
        'pytest-runner',
    ],
)
