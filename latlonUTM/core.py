from pyproj import Proj
from scipy.interpolate import interp1d
import numpy as np


__fun_lon_to_zone = interp1d(np.linspace(-180, 180,61), np.arange(61))
__fun_lat_to_band = interp1d(np.linspace(-80, 80,21), np.arange(21))

def get_zone_and_hemisphere(lat, lon):
    ''' Given a decimal lat/lon position, compute the UTM tiles of this position
    
    Parameters
    ----------
    lat : float
        decimal latitude
    lon : float
        decimal longitude

    Returns
    -------
    (int, str)
       zone number, band character

    In the UTM system, the earth is covered with tiles, which have
    coordinates composed of a number and character. This method identifies
    this coordinate based on the latitude, longitude coordinate.
    '''
    # ensure lon is bewtween -180 and +180 degrees
    # see also wikipedia for more info.
    _lon = (lon + 360)%360
    if _lon>180:
        _lon -= 360
    zone = int(__fun_lon_to_zone(_lon))+1
    band = int(__fun_lat_to_band(lat))
    S = chr(65+4+band)
    return zone, S


def latlon2UTM(lat, lon):
    ''' Converts lat/lon coordinate to UTM x/y

    Parameters
    ----------
    lat : float
        decimal latitude
    lon : float
        decimal longitude

    Returns
    -------
    (float, float), int, str
       a tuple of x,y coordinates in metres easting and northing, zone number and band character.
    '''
    zone, S = get_zone_and_hemisphere(lat, lon)
    p = Proj(proj="utm",
             zone=zone,
             ellps="WGS84",
             south=lat<0)
    return p(lon,lat), zone, S

def UTM2latlon(zone, char, x,y):
    ''' Converts x,y in metres easting/northing for given UTM tile to latitude/longitude.
    
    Parameters
    ----------
    zone : int
        zonal number
    char : str
        band character
    x : float
        metres easting
    y : float
        metres northing

    Returns
    -------
    float, float
        decimal latitude, decimal longitude

    Note
    ----
    The band character is used only to determine the hemisphere 
    (N, O, ..., X: norhtern hemisphere, C, D, ..., M: southern hemisphere.
    '''
    
    p = Proj(proj="utm",
             zone=zone,
             ellps="WGS84",
             south=char<'N')
    lon, lat = p(x,y, inverse=True)
    return lat, lon



def zonalOffset(lat,lon,OriginLongitudeZone=31):
    ''' calculates the zonal offset for lat,lon pair with respect to
        the origin zone, OriginLongitudeZone (default 31). Note that the
        latitude zone is irrelevant as distances are calculated with resp.
        to the equator and correction needs to be applied when hopping from
        one tile to the other.
    '''
    # find out in which tile we live:
    zonalTile=latlon2UTM(lat,lon)[1]
    # the number of tile changes:
    nCrossings=zonalTile-OriginLongitudeZone
    correction=nCrossings*zonalWidth(lat)
    return correction
    
    

def zonalWidth(lat):
    ''' calculates for a specific latitude the zonal width of a tile '''
    lonWest=6.
    lonEast=6.-1e-5

    eastingWest=latlon2UTM(lat,lonWest)[0][0]
    eastingEast=latlon2UTM(lat,lonEast)[0][0]

    width=eastingEast-eastingWest

    return width

def UTM(lat, lon):
    '''
    calculates x and y in metres easting and northing for an array or list
    of lats and lons, all relative to the tile of the first position.
    '''
    P = [latlon2UTM(_lat, _lon) for _lat, _lon in zip(lat, lon)]
    Zone0 = P[0][1]
    offset = [zonalOffset(_lat, _lon, Zone0) for _lat, _lon in zip(lat, lon)]
    x = [_P[0][0] + _offset for _P,_offset in zip(P, offset)]
    y = [_P[0][1] for _P in P]
    return x, y
