from distutils.core import setup
from . import __author__, __version__, __licence__, __doc__

setup(
    name='datapolish',
    version=__version__,
    packages=['', 'graph'],
    url='',
    license=__licence__,
    author=__author__,
    author_email='',
    description=__doc__,
    install_requires=['networkx', 'typing', 'future']
)
