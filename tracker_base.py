import constants

from abstract import Tracker, Point2d, DistanceCalculator2d, FusibleCollection
from geo_calc import euclidean_distance, great_circle_distance, geodesic_distance
from ping import Ping


class TrackerBase(Tracker[Ping]):
    """
    A base tracker class that operates on Ping objects within a fusible collection.

    This class provides basic functionality for tracking Ping objects, including updating the collection of pings
    with new data, setting callsigns for identified pings, and retrieving pings by their unique identifiers.
    The actual storage and fusion logic is delegated to the `FusibleCollection` instance provided during initialization.

    Attributes:
        _threshold (float): The distance threshold used for determining whether pings can be considered identical
                            and therefore fused together.
        _fusible_collection (FusibleCollection[Ping]): The collection that manages the storage, fusion,
                                                       and retrieval of Ping objects.

    Args:
        threshold (float): The distance threshold for fusing pings.
        fusible_collection (FusibleCollection[Ping]): An instance of a class that implements the
                                                      `FusibleCollection` interface for Ping objects.
    """
    _threshold: float
    _fusible_collection: FusibleCollection[Ping]

    def __init__(self, threshold: float, fusible_collection: FusibleCollection[Ping]):
        """
         Initializes a new instance of TrackerBase with a specified threshold and fusible collection.

         Parameters:
             threshold (float): The threshold distance for fusing Ping objects.
             fusible_collection (FusibleCollection[Ping]): The collection that will manage the Pings.
         """
        self._threshold = threshold
        self._fusible_collection = fusible_collection

    def update(self, inputs: list[Ping]) -> tuple[list[tuple[Ping, Ping]], list[Ping]]:
        return self._fusible_collection.fuse(inputs)

    def set_callsign(self, uid: str, callsign: str):
        ping = self.get(uid)
        if ping is not None:
            ping.callsign = callsign

    def get(self, uid: str) -> Ping | None:
        return self._fusible_collection.get(uid)


class Geo2dDistanceCalculator(DistanceCalculator2d):
    """
    A 2D distance calculator that selects the distance calculation method based on a given threshold.

    This class extends `DistanceCalculator2d` to provide a flexible way of calculating distances
    between two points (p1 and p2) in 2D space. It supports Euclidean, great circle, and geodesic
    distance calculations. The choice of method is determined by comparing the provided threshold
    against predefined constants that represent the applicability ranges of each method.

    Attributes:
        _threshold (float): The threshold value used to determine the distance calculation method.

    Args:
        threshold (float): The threshold to use for selecting the distance calculation method.
    """
    _threshold: float

    def __init__(self, threshold: float):
        self._threshold = threshold

    def calculate(self, p1: Point2d, p2: Point2d) -> float:
        if self._threshold < constants.EUCLIDEAN_THRESHOLD:
            return euclidean_distance(p1, p2)
        elif self._threshold < constants.GREAT_CIRCLE_THRESHOLD:
            return great_circle_distance(p1, p2)
        else:
            return geodesic_distance(p1, p2)
