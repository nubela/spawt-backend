#===============================================================================
# geo library
# coordinates are represented by a tuple in the format (lat, long)
#===============================================================================
from kdtree import KDTree

def proximity_sort(point, objects, n_total):
    """
    sort a list of namedtuples by proximity from point, that has a location attribute 
    that returns a tuple of long,lang. returns `n_total` no of objects that are sorted 
    from nearest to furthest
    """
    data_list = (o.location for o in objects)
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