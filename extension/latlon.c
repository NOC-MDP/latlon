// Functions for conversion of lat/lon coordinates to UTM coordinates
// code taken from glider code from Webb Research. See below.
// 20 July 2007, Lucas Merckelbach lmm@noc.soton.ac.uk

// Copyright(c) 2000-2002, Webb Research Corporation, ALL RIGHTS RESERVED
/* latlon.c


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
19-Jun-00 tc@DinkumSoftware.com Switched signs on Longitude
                                <0 ==> west

Table of contents
    latlon_to_utm     These all convert between coordinate systems
    utm_to_latlon

    utm_double_zones_to_str    Converts between <digit><digit><char> and
    utm_str_to_double_zones        two doubles, one for digits, one for char

    private, i.e. static
      is_zone_ok                   checks UTM zone designator for legality


*/

#include "local.h"
#include <stdio.h>
#include "latlon.h"
//#include "mathutil.h"


//WGS-84. See list with file latlong_utm.c/h
static const int RefEllipsoid = 23;

// private functions
static bool is_zone_ok(int zone_num, char zone_char) ;



/* latlon_to_utm

Converts lat/lon to zone/northing/easting

    lat:    degrees minutes.decimal_minutes (north positive)
    lon:    degrees minutes.decimal_minutes (east positive)
            xxyy.zzz    xx degs yy minutes zzz fractions of minute

	zone_num: positive number corresponds to <digit><digit> of zone
	zone_char: postiive number corresponding to <char> of zone.
	           0-A, 1-B, etc
	

Normally returns false, returns true on error.

29-May-00 tc@DinkumSoftware.com Initial
05-Jun-00 tc@DinkumSoftware.com Shifted lat/long 2 digits
19-Jun-00 tc@DinkumSoftware.com Switched signed on west longitude
                                <0 ==> West
*/

bool latlon_to_utm( double lat, double lon,
                   double *zone_num, double *zone_char,
                   double *northing, double *easting)
{
  bool is_err ;    // what we return
  double lat_as_decimal_degrees, lon_as_decimal_degrees ;
  char zone_as_str[UTMZone_max_strlength] ;

  // convert degrees.decimal_minutes to decimal_degrees
  // lat_as_decimal_degrees = degs_dec_minutes_to_dec_degrees(lat) ;
  // lon_as_decimal_degrees = degs_dec_minutes_to_dec_degrees(lon) ;
  lat_as_decimal_degrees = lat ;
  lon_as_decimal_degrees = lon ;

  // Use someone else to do the work
  LLtoUTM(RefEllipsoid,
          lat_as_decimal_degrees, lon_as_decimal_degrees,
          northing, easting, zone_as_str) ;

  // Convert the zone to a pair of doubles
  // In: <digit><digit><char>
  is_err = utm_str_to_double_zones(zone_as_str,
                                   zone_num, zone_char) ;

  // tell um no errors
  return is_err ;

}


/* utm_to_latlon

Converts:
    zone_num    positive number corresponding to <digit><digit> of zone
    zone_char   positive number correspond to <char>, 0-A, 1-B etc
    northing/easting

to
    lat:    degrees minutes.decimal_minutes (north positive)
    lon:    degrees minutes.decimal_minutes (east positive)
            xxyy.zzz    xx degs yy minutes zzz fractions of minute

Normally returns false, returns true on error.

29-May-00 tc@DinkumSoftware.com Initial
05-Jun-00 tc@DinkumSoftware.com Shifted lat/long 2 digits
19-Jun-00 tc@DinkumSoftware.com Switched signed on west longitude
                                <0 ==> West
*/

bool utm_to_latlon( double zone_num, double zone_char, double northing, double easting,
                   double *lat, double *lon)
{
  bool is_err ;
  double lat_as_decimal_deg, lon_as_decimal_deg ;  // intermediate output
  char zone_as_str[UTMZone_max_strlength] ;

  // In case of error
  *lat = *lon = 0.0 ;

  // Convert our zone from pair of doubles to character string
  is_err = utm_double_zones_to_str( zone_num, zone_char, zone_as_str) ;
  if ( is_err )
    return true ;

  // Let someone else do the work
  UTMtoLL(RefEllipsoid,
          northing, easting, zone_as_str,
          &lat_as_decimal_deg, &lon_as_decimal_deg) ;


  // Convert from decimal degrees to degrees and decimal minutes
  //*lat = dec_degrees_to_degs_dec_minutes(lat_as_decimal_deg) ;
  //*lon = dec_degrees_to_degs_dec_minutes(lon_as_decimal_deg) ;
  *lat = lat_as_decimal_deg ;
  *lon = lon_as_decimal_deg ;

  // tell um no error
  return false ;
}


/* utm_double_zones_to_str
   utm_str_to_double_zones


These convert the UTM zone designator back and forth between a character string
and two doubles.

    19C    <-->    19.0    zone_num,  e.g. 19
                    2.0    zone_char, e.g.  C  (0->A, 1->B, 2->C etc)

"str" should be at least "UTMZone_max_strlength" characters long.

Each normally returns false, but returns true to indicate an error.

All this silliness is because we can only store doubles as sensor values.

29-May-00 tc@DinkumSoftware.com Initial

*/


bool utm_double_zones_to_str(double zone_num, double zone_char, char *str)
{
  int zone_num_as_int  = zone_num ;    // convert input args
  int zone_char_as_int = zone_char ;
  char zone_char_as_char = zone_char_as_int + 'A' ;

// error check
  if ( !is_zone_ok( zone_num_as_int, zone_char_as_char) )
  {  // error
     str[0] = '\0' ;
     return true ;
  }

  // Put um together as a string
  sprintf ( str, "%02d%c", zone_num_as_int, zone_char_as_char) ;

  return false ;    // say no error
}

bool utm_str_to_double_zones( const char * str, double * zone_num, double *zone_char)
{
  int zone_num_as_int ;
  char zone_char_as_char ;
  int num_cnvrted ;    // working

  // In case of error
  *zone_num = *zone_char = -1.0 ;

  // Split apart the zone number and character
  num_cnvrted = sscanf( str, "%d%c", &zone_num_as_int, &zone_char_as_char) ;
  if ( num_cnvrted != 2 )
    // error
    return true ;


  // error check
  if ( !is_zone_ok( zone_num_as_int, zone_char_as_char) )
  {  // error
     return true ;
  }

  // Put them to doubles
  *zone_num  = zone_num_as_int ;
  *zone_char = zone_char_as_char - 'A' ;

  return false ;    // say no error
}


/* is_zone_ok

Checks "zone_num" and "zone_char" for being legal
UTM designator:

    zone_num:    0 to 60 inclusive
    zone_char:   C to X inclusive

Normally returns true if all is good and
false on error.

29-May-00 tc@DinkumSoftware.com Initial

*/

bool is_zone_ok(int zone_num, char zone_char)
{
  // Zone letters run C to X inclusive
  if ( (zone_char < 'C') ||
       (zone_char > 'X') )
  {   // error
      return false ;
  }
  
  // Zone numbers run 0 to 60 inclusive
  if ( (zone_num <  0) ||
       (zone_num > 60) )
  {    // error
       return false ;
  }

  // all is ok
  return true ;

}
