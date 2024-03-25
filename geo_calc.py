import constants

from geopy.distance import geodesic, great_circle

from abstract import Point2d


def geodesic_distance(p1: Point2d, p2: Point2d) -> float:
    """
    Calculate the geodesic distance between two points on the Earth's surface.

    Parameters:
        p1 (tuple[float, float]): The first point as a (latitude, longitude) tuple.
        p2 (tuple[float, float]): The second point as a (latitude, longitude) tuple.

    Returns:
        float: The distance between the two points in meters.
    """
    return geodesic(p1, p2).meters


def euclidean_distance(p1: Point2d, p2: Point2d) -> float:
    """
    Calculate the Euclidean distance between two points.

    Note: This calculation assumes a flat Earth and does not take into account
    the Earth's curvature, making it suitable for short distances.

    Parameters:
        p1 (tuple[float, float]): The first point as a (latitude, longitude) tuple.
        p2 (tuple[float, float]): The second point as a (latitude, longitude) tuple.

    Returns:
        float: The Euclidean distance between the two points in meters, assuming
               each degree of latitude or longitude is approximately 111,139 meters.
    """
    lat1, lon1 = p1
    lat2, lon2 = p2
    distance_deg: float = ((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) ** 0.5

    return distance_deg * constants.DEGREES_TO_METERS


# great_circle_distance: Calculate the great circle distance between two points and return the distance in meters
def great_circle_distance(p1: Point2d, p2: Point2d) -> float:
    """
    Calculate the great circle distance between two points on the Earth's surface.

    Parameters:
        p1 (tuple[float, float]): The first point as a (latitude, longitude) tuple.
        p2 (tuple[float, float]): The second point as a (latitude, longitude) tuple.

    Returns:
        float: The great circle distance between the two points in meters.
    """
    return great_circle(p1, p2).meters
