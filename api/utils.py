import math

def haversine_distance(lat1, long1, lat2, long2):
    """
    Calculates the Haversine distance between two points
    on the earth's surface.
    
    The Haversine distance is the great-circle distance between 
    two points on a sphere. It is defined as the shortest
    distance between two points on a sphere that is calculated along 
    the surface of the sphere (as opposed to a straight
    line through the sphere's interior). The Haversine distance formula 
    is used to calculate the distance between two
    points on the earth's surface given their latitude and longitude coordinates.
    
    Parameters
    ----------
    lat1 : float
        Latitude of the first point in degrees.
    long1 : float
        Longitude of the first point in degrees.
    lat2 : float
        Latitude of the second point in degrees.
    long2 : float
        Longitude of the second point in degrees.
        
    Returns
    -------
    float
        The Haversine distance between the two points in kilometers.
        
    Examples
    --------
    >>> haversine_distance(37.7749, -122.4194, 40.7128, -74.0060)
    3959.897153568822
    """
    # convert latitude and longitude to radians
    lat1, long1, lat2, long2 = map(math.radians, [lat1, long1, lat2, long2])
    
    # apply Haversine formula
    dlat = lat2 - lat1
    dlong = long2 - long1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlong/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of the earth in km
    return c * r

def average_haversine_distance(points):
    """
    Calculate the average haversine distance between
    consecutive points in a list of points.
    Arguments:
    points -- a list of points, where each point is a list of
    two values representing the latitude and longitude.
    Returns:
    The average haversine distance between consecutive points in
    the list in kilometers.
    """
    total_distance = 0
    num_pairs = 0

    for i in range(len(points) - 1):
        lat1, lon1 = points[i]
        lat2, lon2 = points[i+1]
        distance = haversine_distance(lat1, lon1, lat2, lon2)
        total_distance += distance
        num_pairs += 1

    if num_pairs == 0:
        return 0

    return total_distance / num_pairs


def match_routes(route1, route2, threshold=0.05):
    """
    This function calculates the match rate between two routes.
    The match rate is defined as the number of points in the shorter
    route that are within a  certain distance threshold from the points
    in the longer route. The haversine distance is used to calculate the
    distance between two points.
    
    Parameters:
    route1 (list of tuples): A list of tuples, where each tuple contains the
    			     latitude and longitude of a point in the first route.
    route2 (list of tuples): A list of tuples, where each tuple contains the latitude
    			     and longitude of a point in the second route.
    threshold (float): The maximum distance (in kilometers) that two points can be
    		       apart to be considered a match. The default value is 0.05 km.
    		       Ideally, the threshold should be selected so that it's less than
    		       the avg haversine distance between successive points in a route and big
    		       enough to account for slight variations in the point coordinates(errors)
    
    Returns:
    float: The match rate between the two routes, expressed as a decimal value between 0 and 1.
    
    Example:
    >>> route1 = [(51.5074, 0.1278), (51.5080, 0.1279), (51.5082, 0.1280)]
    >>> route2 = [(51.5073, 0.1278), (51.5080, 0.1279), (51.5082, 0.1280), (51.5083, 0.1281)]
    >>> match_routes(route1, route2)
    0.6666666666666666
    """
    shorter_route = route1 if len(route1) <= len(route2) else route2
    longer_route = route2 if len(route1) <= len(route2) else route1
    match = 0
    # Dynamically calculate threshold
    # avg_hv1 = average_haversine_distance(shorter_route)
    # avg_hv2 = average_haversine_distance(longer_route)
    # theeshold = (avg_hv1 + avg_hv2) / 2

    for i, (lat1, lon1) in enumerate(shorter_route):
        for j, (lat2, lon2) in enumerate(longer_route):
            if haversine_distance(lat1, lon1, lat2, lon2) <= threshold:
                match += 1
                break
    match_rate = match / len(shorter_route)
    return match_rate
