#===============================================================================
# geo library
# coordinates are represented by a tuple in the format (lat, long)
#===============================================================================
from kdtree import KDTree
from math import sin, cos, asin, sqrt, degrees, radians

Earth_radius_km = 6371.0
RADIUS = Earth_radius_km

def proximity_sort(point, objects, n_total):
    """
    sort a list of namedtuples by proximity from point, that has a location attribute 
    that returns a tuple of long,lang. returns `n_total` no of objects that are sorted 
    from nearest to furthest
    """
    data_list = [o.location for o in objects]
    sorted_location = _proximity_filter(point, data_list, n_total)
    sorted_obj = []
    for l in sorted_location:
        for o in objects:
            if not o in sorted_obj and o.location == l:
                sorted_obj += [o]
                
    return sorted_obj

def _proximity_filter(point, data, total):
    """
    Given a point, and a data list of coordinate tuples, we return an n number of coordinate tuples
    amounting to total
    """
    tree = KDTree.construct_from_data(data)
    return tree.query(query_point=point, t=total)

def haversine(angle_radians):
    return sin(angle_radians / 2.0) ** 2

def inverse_haversine(h):
    return 2 * asin(sqrt(h)) # radians

def distance_between_points(lat1, lon1, lat2, lon2):
    """
    all args are in degrees
    WARNING: loss of absolute precision when points are near-antipodal
    """
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    dlat = lat2 - lat1
    dlon = radians(lon2 - lon1)
    h = haversine(dlat) + cos(lat1) * cos(lat2) * haversine(dlon)
    return RADIUS * inverse_haversine(h)

def bounding_box(lat, lon, distance_km):
    """
    Input and output lats/longs are in degrees.
    Distance arg must be in same units as RADIUS.
    Returns (dlat, dlon) such that
    no points outside lat +/- dlat or outside lon +/- dlon
    are <= "distance" from the (lat, lon) point.
    Derived from: http://janmatuschek.de/LatitudeLongitudeBoundingCoordinates
    WARNING: problems if North/South Pole is in circle of interest
    WARNING: problems if longitude meridian +/-180 degrees intersects circle of interest
    See quoted article for how to detect and overcome the above problems.
    Note: the result is independent of the longitude of the central point, so the
    "lon" arg is not used.
    """
    dlat = distance_km / RADIUS
    dlon = asin(sin(dlat) / cos(radians(lat)))
    return float(degrees(dlat)), float(degrees(dlon))