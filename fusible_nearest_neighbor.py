from copy import copy

from mypy.checker import Union

from abstract import DistanceCalculator2d, FusibleCollection
from ping import Ping
from tracker_base import Geo2dDistanceCalculator


class PingList(FusibleCollection[Ping]):
    """
    Concrete implementation of FusibleCollection for managing and fusing Ping objects in a list based on proximity.

    This class maintains a list of Ping objects and provides functionality to add new Pings, fuse them based on
    geographic proximity determined by a specified distance threshold, and retrieve them by unique identifier.
    Fusion of Pings is performed using a DistanceCalculator2d to compare distances and decide on fusions.

    Attributes:
        _tracks (list[Ping]): List of Ping objects being managed.
        _threshold (float): Threshold distance for determining when two Pings should be fused.
        distancer (DistanceCalculator2d): Distance calculator for comparing the distances between Ping objects.

    Methods:
        __init__: Initializes a new PingList with a specified threshold for fusion.
        put: Adds a Ping to the list or fuses it with an existing Ping based on proximity.
        fuse: Fuses Ping objects in the given list based on geographic proximity.
        get: Retrieves a Ping object by its unique identifier.
        remove_duplicates: Removes duplicate Ping objects from the list based on proximity.
        get_closest_ping_index: Finds the index of the Ping closest to a given Ping.
    """
    _tracks: list[Ping]
    _threshold: float
    distancer: DistanceCalculator2d

    def __init__(self, threshold: float):
        self._threshold = threshold
        self._tracks = []
        self.distancer = Geo2dDistanceCalculator(threshold)

    def put(self, ping: Ping) -> list[Ping]:
        closest_ping_index = self.get_closest_ping_index(self._tracks, ping)
        if closest_ping_index is not None:
            matched = [copy(self._tracks[closest_ping_index]), copy(ping)]
            self._tracks[closest_ping_index] = self._tracks[closest_ping_index].merge(ping)
            return matched
        else:
            self._tracks.append(ping)
            return [copy(ping)]

    def fuse(self, object_list: list[Ping]) -> tuple[list[tuple[Ping, Ping]], list[Ping]]:
        sanitized: list[Ping] = self.remove_duplicates(object_list)
        matched: list[tuple[Ping, Ping]] = []
        already_matched: set[str] = set()
        unmatched: list[Ping] = []
        for i in range(0, len(sanitized)):
            # check the matches to see if we have already matched this ping
            if sanitized[i].track_id in already_matched:
                continue

            res = self.put(sanitized[i])
            if len(res) > 1:
                matched.append((copy(res[0]), copy(res[1])))
                already_matched.add(res[0].track_id)
                already_matched.add(res[1].track_id)
            else:
                unmatched.append(res[0])
        return matched, unmatched

    # get: Get a ping with a given uid
    def get(self, uid: str) -> Ping | None:
        for ping in self._tracks:
            if ping.track_id == uid:
                return ping
        return None

    # remove_duplicates: Remove pings in the same range from a list of pings recursively
    def remove_duplicates(self, inputs: list[Ping]) -> list[Ping]:
        for i in range(len(inputs)):
            for j in range(i + 1, len(inputs)):
                if self.distancer.calculate((inputs[i].latitude, inputs[i].longitude),
                                            (inputs[j].latitude, inputs[j].longitude)) < self._threshold:
                    inputs[i] = inputs[i].merge(inputs[j])
                    inputs.pop(j)
                    return self.remove_duplicates(inputs)
        return inputs

    # get_closest_ping_index: Get the index of the closest ping in a list of pings
    def get_closest_ping_index(self, ping_list: list[Ping], new_ping: Ping) -> int | None:
        closest_ping: Union[int, None] = None
        closest_dist: float = self._threshold
        for i, ping in enumerate(ping_list):
            dist = self.distancer.calculate((ping.latitude, ping.longitude), (new_ping.latitude, new_ping.longitude))
            if dist < closest_dist:
                closest_dist = dist
                closest_ping = i
        return closest_ping
