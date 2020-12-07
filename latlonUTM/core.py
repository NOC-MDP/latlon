from _latlonUTM import *

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
