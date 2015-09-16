from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from distutils.core import setup

setup (name = 'latlon',
       version = '0.3',
       description = 'A bundle of classes useful when working with lat/lon coordinates',
       author = 'Lucas Merckelbach',
       author_email = 'lmm@noc.soton.ac.uk',
       url = '',
       py_modules=['latlon','gps'],
       packages = [],
       long_description ='A bundle of classes useful when working with lat/lon coordinates')



