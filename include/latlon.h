// Copyright(c) 2000-2002, Webb Research Corporation, ALL RIGHTS RESERVED
/* latlon.h

Has conversion functions between lat/lon and UTM.

Ideally this code belongs in coord_sys.h ... but
there were some host side test programs which call
these functions that wouldn't link with coord_sys.c because
of all the target dependencies, so there were separated into this
file.

All the REAL work is done in latlong_utm.c/h which was downloaded
from the net.  These functions are thin layers which between the
application code and latlong_utm.c/h.  The intent was to keep the
code downloaded from the net "pristine", i.e. as unmodified as
possible.

05-Jun-00 tc@DinkumSoftware.com Initial

*/

#ifndef LATLON_H
#define LATLON_H

#include "latlong_utm.h"    // for UTMZone_max_strlength

// Convert lat/long -> utm
bool latlon_to_utm( double lat, double lon,
                    double *zone_num, double *zone_char,
                    double *northing, double *easting) ;

// Convert utm -> lat/long
bool utm_to_latlon( double zone_num, double zone_char,
                    double northing, double easting,
                    double *lat, double *lon) ;


// UTM zone changes
bool utm_double_zones_to_str(double zone_num, double zone_char, char *str) ;
bool utm_str_to_double_zones( const char * str, double * zone_num, double *zone_char) ;


#endif // LATLON_H
