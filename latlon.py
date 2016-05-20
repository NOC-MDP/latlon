''' Module that provides classes for use with lat lon coordinates.

module methods:
   conversions to decimal and nmea formats
convertToDecimal()
convertToNmea()

classes:
LatLon - for defining lat/lon coordinates
'''
from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from builtins import zip
from builtins import int
from future import standard_library
standard_library.install_aliases()
from builtins import object



import sys
import numpy as N
try:
    import latlonUTM
except ImportError:
    sys.stderr.write("Warning: Could not import module latlonUTM.\n")
    sys.stderr.write("Warning: Using LatLon class will fail. Use LL instead.\n")


# module methods.

def __convertToDecimal(x):
    ''' Converts a latitiude or longitude in NMEA format to decimale degrees'''
    sign=N.sign(x)
    xAbs=N.abs(x)
    degrees=N.floor(xAbs/100.)
    minutes=xAbs-degrees*100
    decimalFormat=degrees+minutes/60.
    return decimalFormat*sign

def __convertToNmea(x):
    ''' Converts a latitude or longitude in decimal format to NMEA format.'''
    sign=N.sign(x)
    xAbs=N.abs(x)
    degree=N.floor(xAbs)
    minutes=xAbs-degree
    nmeaFormat=degree*100+minutes*60
    return nmeaFormat*sign


def convertToDecimal(x,y=None):
    ''' Converts a latitiude or longitude in NMEA format to decimale degrees, or a pair
        given in x,y'''
    if not y==None:
        X=__convertToDecimal(x)
        Y=__convertToDecimal(y)
        return X,Y
    return __convertToDecimal(x)

def convertToNmea(x,y=None):
    ''' Converts a latitude or longitude in decimal format to NMEA format.'''
    if not y==None:
        X=__convertToNmea(x)
        Y=__convertToNmea(y)
        return X,Y
    return __convertToNmea(x)

# classes

class LL(object):
    R=12742e3/2.

    def __str__(self):
        if self.format==self.initial_format:
            return "%f %f"%(self.lat,self.lon)
        else:
            if self.format=='nmea':
                tmp=convertToNmea([self.lat,self.lon])
            else:
                tmp=convertToDecimal([self.lat,self.lon])
            return "%f %f"%(tmp[0],tmp[1])

    def __init__(self,lat,lon,format='decimal'):
        if not format in ['decimal','nmea']:
            raise ValueError("lat/lon format should be either 'decimal' or 'nmea'")
        self.format=format
        if format=='decimal':
            self._lat=lat
            self._lon=lon
        else:
            self._lat,self._lon=convertToDecimal(lat,lon)
        self.dx=None
        self.dy=None

        _lon=self._toRad(self._lon)
        _lat=self._toRad(self._lat)
        self._v=N.matrix([N.cos(_lon)*N.cos(_lat),
                          N.sin(_lon)*N.cos(_lat),
                          N.sin(_lat)])

    def __call__(self):
        return self._lat,self._lon

    @property
    def lat(self):
        if self.format=='nmea':
            return convertToNmea(self._lat)
        else:
            return self._lat

    @property
    def lon(self):
        if self.format=='nmea':
            return convertToNmea(self._lon)
        else:
            return self._lon

    def set_lat(self,lat):
        if self.format=="nmea":
            self._lat=convertToDecimal(lat)
        else:
            self._lat=lat

    def set_lon(self,lon):
        if self.format=="nmea":
            self._lon=convertToDecimal(lon)
        else:
            self._lon=lon

    def set_latlon(self,lat,lon):
        self.set_lat(lat)
        self.set_lon(lon)


    def _toRad(self,x):
        return x*N.pi/180.

    def nmea(self):
        return convertToNmea(self._lat,self._lon)

    def standard_string(self):
        if self._lat>0:
            lat_modifier = "N"
        else:
           lat_modifier = "S"
        if self._lon>0:
            lon_modifier = "E"
        else:
            lon_modifier = "W"
        lat_nmea,lon_nmea = convertToNmea(abs(self._lat),abs(self._lon))
        lat_deg = int(lat_nmea/100)
        lon_deg = int(lon_nmea/100)
        lat_min = lat_nmea - 100*lat_deg
        lon_min = lon_nmea - 100*lon_deg
        return ("%02d%s%6.3f"%(lat_deg,lat_modifier,lat_min),
                "%02d%s%6.3f"%(lon_deg,lon_modifier,lon_min))
        

    def distance(self,p):
        cs=(self._v*p._v.T)[0,0]
        if cs>=1:
            r=0
        elif cs<=-1:
            r=N.pi
        else:
            r=N.arccos(cs)*self.R
        if not N.isfinite(r):
            raise ValueError
        return r

    @property
    def Rot(self):
        phi=-self._toRad(self._lon)
        r=N.matrix([[N.cos(phi),N.sin(phi),0],
                    [-N.sin(phi),N.cos(phi),0],
                    [0,           0          ,1]])
        return r

    def bearing(self,p):
        PcrossQ=N.cross(self._v,p._v)
        PcrossQp=PcrossQ*self.Rot
        Evector=N.matrix([0,1.,0])
        _lat=self._toRad(self._lat)
        _lon=self._toRad(self._lon)
        #is this correct???
        Nvector=N.matrix([-N.sin(_lat),0,N.cos(_lat)])
        y=(PcrossQp*Nvector.T)[0,0]
        x=(PcrossQp*Evector.T)[0,0]
        phi=N.arctan2(y,x)
        return (180-phi*180./N.pi+360)%360


class LatLon(object):
    ''' generic class for lat/lon data.
      called with lat, lon given as decimal (default) or in nmea format. In latter
      case the format='nmea' option should be given.
      
      methods to convert between decimal and nmea representation and distance
      calcultion with other lat lon point.
   '''
    def __init__(self,lat,lon,format='decimal'):
        if not format in ['decimal','nmea']:
            raise ValueError("lat/lon format should be either 'decimal' or 'nmea'")
        self.format=format
        if format=='decimal':
            self._lat=lat
            self._lon=lon
        else:
            self._lat,self._lon=convertToDecimal(lat,lon)
        self.dx=None
        self.dy=None

    def __call__(self):
        return self._lat,self._lon

    def nmea(self):
        return convertToNmea(self._lat,self._lon)

    def standard_string(self):
        if self._lat>0:
            lat_modifier = "N"
        else:
           lat_modifier = "S"
        if self._lon>0:
            lon_modifier = "E"
        else:
            lon_modifier = "W"
        lat_nmea,lon_nmea = convertToNmea(abs(self._lat),abs(self._lon))
        lat_deg = int(lat_nmea/100)
        lon_deg = int(lon_nmea/100)
        lat_min = lat_nmea - 100*lat_deg
        lon_min = lon_nmea - 100*lon_deg
        return ("%02d%s%06.3f"%(lat_deg,lat_modifier,lat_min),
                "%02d%s%06.3f"%(lon_deg,lon_modifier,lon_min))

    @property
    def lat(self):
        if self.format=='nmea':
            return convertToNmea(self._lat)
        else:
            return self._lat

    @property
    def lon(self):
        if self.format=='nmea':
            return convertToNmea(self._lon)
        else:
            return self._lon

    def set_lat(self,lat):
        if self.format=="nmea":
            self._lat=convertToDecimal(lat)
        else:
            self._lat=lat

    def set_lon(self,lon):
        if self.format=="nmea":
            self._lon=convertToDecimal(lon)
        else:
            self._lon=lon

    def set_latlon(self,lat,lon):
        self.set_lat(lat)
        self.set_lon(lon)

    def calculateDxDy(self,P):
        ''' calculates dx and dy.
        P is a LatLon instance
        '''
        # convert to metres.
        ((x0,y0),zone0,band0)=latlonUTM.latlon2UTM(self._lat,self._lon)
        y0-=10000000*int(band0<='M') # correct for the false northin
                                    # when on southern hemisphere band
                                    # <=M
        # now for the second point
        ((x1,y1),zone1,band1)=latlonUTM.latlon2UTM(P._lat,P._lon)   
        y1-=10000000*int(band1<='M') # correct for the false northing
        offset=latlonUTM.zonalOffset(P._lat,P._lon,zone0)
        x1+=offset
        self.dx=x1-x0
        self.dy=y1-y0
        return self.dx,self.dy

    def distance(self,P):
        self.calculateDxDy(P)
        R=N.sqrt((self.dx)**2+(self.dy)**2)
        # in case we converted the lat/lon points
        return R

    def bearing(self,P):
        ''' calculates the bearing with current point and point given in argument.
           the argument can be either a LatLon instance or lat,lon in decimal notation.
        '''
        self.calculateDxDy(P)
        R=-N.arctan2(self.dy,self.dx)*180./N.pi+90
        R=(R+360.)%360.
        return R

    def UTM(self,correctOffset=True):
        ''' returns latlon position(s) into UTM coordinates. if correctOffset, all positions
           are calculated relative to the zone of the first position.
        '''
        if N.isscalar(self._lat) and N.isscalar(self._lon):
            # assume we are dealing with a single point.
            R=latlonUTM.latlon2UTM(self._lat,self._lon)
            return R
        else: # assume we are dealing with arrays.
            positions=[]
            zones=[]
            zonesAlt=[]
            for lt,ln in zip(self._lat,self._lon):
                R=latlonUTM.latlon2UTM(lt,ln)
                zones.append(R[1])
                zonesAlt.append(R[2])
                if correctOffset:
                    offset=latlonUTM.zonalOffset(lt,ln,zones[0])
                else:
                    offset=0
                positions.append((R[0][0]+offset,R[0][1]))
            return positions,zones,zonesAlt

    def translate(self,dx,dy):
        ''' translates a waypoint of dx (east), dy (north) '''
        UTM=latlonUTM.latlon2UTM(self._lat,self._lon)
        zone=UTM[1]
        UTMx=UTM[0][0]
        UTMy=UTM[0][1]
        # translate the UTM coordinates.
        UTMx+=dx
        UTMy+=dy
        newLatLon=latlonUTM.UTM2latlon(UTM[1],UTM[2],UTMx,UTMy)
        lat=newLatLon[0]
        lon=newLatLon[1]
        return LatLon(lat,lon,"decimal")




if __name__=="__main__":
    P=LatLon(54,8,'decimal')
    Q=LatLon(5500,800,'nmea')
    print(P.distance(Q))
    print(P.bearing(Q))

    p=LL(54,8,'decimal')
    q=LL(5500,800,'nmea')
    print(p.distance(p))
    print(q.bearing(q))
