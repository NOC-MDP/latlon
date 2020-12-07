// Copyright(c) 2000-2002, Webb Research Corporation, ALL RIGHTS RESERVED
/* latlong_utm.h

This is a collection of routines for converting lat/long to UTM
coordinates.  The original source code in C++ was downloaded from:
    http://www.gpsy.com/gpsinfo/geotoutm/index.html
        constants.h
        LatLong-UTMconversion.cpp
        LatLong-UTMconversion.h
        SwissGrid.cpp
        UTMConversions.cpp           the main() of short test program

I did NOT convert the "swissgrid" code.  I think it's some kind of
special coordinate system that only works in Switzerland.  As this
work is being done for the Webb Research glider, I don't think we'll
miss this.

I'm frankly not sure who wrote this originally.  I think it was
    Chuck Gantz- chuck.gantz@globalstar.com
I translated it from C++ to C.  The attributions I found in the source follow
    26-May-00 tc@DinkumSoftware.com 
----------------------------------------------------------------------

Reference ellipsoids derived from Peter H. Dana's website- 
http://www.utexas.edu/depts/grg/gcraft/notes/datum/elist.html
Department of Geography, University of Texas at Austin
Internet: pdana@mail.utexas.edu
3/22/95

Source
Defense Mapping Agency. 1987b. DMA Technical Report: Supplement to Department of Defense World Geodetic System
1984 Technical Report. Part I and II. Washington, DC: Defense Mapping Agency

Written by Chuck Gantz- chuck.gantz@globalstar.com


26-May-00 tc@DinkumSoftware.com Initial

*/

#ifndef LATLONG_UTM_H

void LLtoUTM(int ReferenceEllipsoid,
             const double Lat, const double Long, 
			 double * UTMNorthing, double * UTMEasting, char* UTMZone);
void UTMtoLL(int ReferenceEllipsoid,
             const double UTMNorthing, const double UTMEasting, const char* UTMZone,
			 double *  Lat,  double * Long );


#define    UTMZone_max_strlength    10    // I think 4 is all that is required:
                                          // <digit><digit><letter><null>
                                          // but memory is cheap

#endif
