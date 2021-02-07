#!/usr/bin/env python

import os
from setuptools import find_packages, setup, Extension


about = {'name':"latlon"}


with open(f"{about['name']}/_version.py", encoding="utf-8") as f:
    exec(f.read(), about)

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), encoding='utf8') as fh:
    long_description = fh.read()

with open('requirements.txt') as fobj:
    install_requires = [line.strip() for line in fobj]


latlonUTM_ext = Extension('_latlonUTM',
                          define_macros = [('MAJOR_VERSION', '0'),
                                           ('MINOR_VERSION', '1')],
                          include_dirs = ['./include'],
                          libraries = [],
                          library_dirs = ['.'],
                          sources = ['extension/_latlonUTMmodule.c',\
                                     'extension/latlon.c',\
                                     'extension/latlong_utm.c'])

setup(
    name=about['name'],
    version=about['__version__'],
    description='Lat/lon and UTM utilities',
    long_description=long_description,
    url='https://github.com/',
    author='Lucas Merckelbach',
    author_email='lucas.merckelbach@hzg.de',
    license='GPLv3',
    packages=find_packages(where='.', exclude=['tests', 'docs', 'examples']),
    ext_modules = [latlonUTM_ext],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GPLv3 License',
        'Environment :: Console',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.9',
    ],
    keywords=['ocean gliders', 'glider flight', 'oceanography'],
    install_requires=install_requires,
    include_package_data=True,
    #scripts=[''],
    #py_modules=[''],

)
# how to provide scripts etct
#      py_modules = ['fastachar'],
#      entry_points = {'console_scripts':[],#['fastachar_gui = fastachar_gui:main
#                      'gui_scripts':['fastachar = fastachar:main']
#                      },


