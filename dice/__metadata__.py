# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

__all__ = (
    '__name__', '__description__', '__version__', '__author__',
    '__author_email__', '__maintainer__', '__maintainer_email__',
    '__copyright_years__', '__license__', '__url__', '__ver__',
    '__classifiers__', '__keywords__', 'package_metadata',
)

# ----------------------------------------------------------------------
# Package Metadata
# ----------------------------------------------------------------------
__name__ = 'dice'
__description__ = 'A DSL for dice notation built in python'
__version__ = '0.3.0'

__author__ = 'Brian Bruggeman'
__author_email__ = 'brian.m.bruggeman@gmail.com'

__maintainer__ = __author__
__maintainer_email__ = __author_email__

__copyright_years__ = '2017'
__license__ = 'Apache 2.0'
__url__ = 'https://github.com/brianbruggeman'
__ver__ = tuple([int(ver_i.split('-')[0]) for ver_i in __version__.split('.')])

__classifiers__ = [
    'Programming Language :: Python',
    'Natural Language :: English',
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: Other/Proprietary License',
    'Natural Language :: English',
    'Operating System :: POSIX',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: Implementation :: CPython',
    'Topic :: Software Development',
]

__keywords__ = ['dice', 'dsl', 'd20', 'dice notation']

# Package everything above into something nice and convenient for extracting
package_metadata = {k.strip('_'): v for k, v in locals().items() if k.startswith('__') and k != '__all__'}
if '__doc__' in locals():
    package_metadata['doc'] == __doc__
