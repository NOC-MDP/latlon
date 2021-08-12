Latlon/latlonUTM package
========================

Synopsis
--------

Some utilities to work with coordinates in latitude and longitude.

This module provides two packages, namely latlon and latlonUTM.

The latlonUTM package provides a way to translate a latitude longitude
coordinate to a Universal Transfer Mercator (UTM) coordinate, see also
Wikipedia https://en.wikipedia.org/wiki/Universal_Transverse_Mercator_coordinate_system.

The latlon package introduces a class that represents a position in
latitude and longitude. Methods are provided to compute the distance
between points, the direction from one point to another, translate
points etc.

Distance calculations are based on the latlonUTM package.

Transformation between lat/lon and UTM is now based on utm, in 
favour of a C extension. Pyproj has been considered but was found too
slow.