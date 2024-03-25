# PingGeoHash: A class that stores pings in a dictionary with the key being the geohash of the lat long
import math
from copy import copy

import constants
import pygeohash as pgh
from abstract import FusibleCollection
from ping import Ping


class PingGeoHash(FusibleCollection[Ping]):
    """
    Concrete implementation of the FusibleCollection for Ping objects, utilizing geohashing for fusion.

    This class manages a collection of Ping objects, offering functionality to add pings to a geohash-based
    collection, fuse them based on geographic proximity determined by a specified precision threshold, and
    retrieve them by a unique identifier.

    Attributes:
        geo_hash (dict[str, Ping]): A dictionary mapping geohash keys to Ping objects.
        _precision (int): The precision level of geohashing, dynamically determined by a threshold.
        geo_hash_precisions (dict[int, range]): A mapping of geohash precision levels to their corresponding
                                                resolution ranges.

    Methods:
        __init__: Initializes a new instance of PingGeoHash with a specified threshold for geohash precision.
        precision: Property that returns the current geohash precision of the collection.
        generate_precision: Determines the appropriate geohash precision based on a given threshold.
        put: Adds a Ping to the collection, possibly fusing it with an existing Ping based on geohash proximity.
        remove_duplicates: Helper method to remove duplicate Pings based on geohash keys.
        fuse: Implements the fusion of Ping objects based on geohash proximity.
        get: Retrieves a Ping object by its unique identifier.
    """
    geo_hash: dict[str, Ping]
    _precision: int
    geo_hash_precisions: dict[int, range] = {
        2: range(constants.GEO_HASH_PRECISION_2_RESOLUTION, constants.GEO_HASH_PRECISION_1_RESOLUTION),  # precision 2
        3: range(constants.GEO_HASH_PRECISION_3_RESOLUTION, constants.GEO_HASH_PRECISION_2_RESOLUTION),  # precision 3
        4: range(constants.GEO_HASH_PRECISION_4_RESOLUTION, constants.GEO_HASH_PRECISION_3_RESOLUTION),  # precision 4
        5: range(constants.GEO_HASH_PRECISION_5_RESOLUTION, constants.GEO_HASH_PRECISION_4_RESOLUTION),  # precision 5
        6: range(constants.GEO_HASH_PRECISION_6_RESOLUTION, constants.GEO_HASH_PRECISION_5_RESOLUTION),  # precision 6
        7: range(constants.GEO_HASH_PRECISION_7_RESOLUTION, constants.GEO_HASH_PRECISION_6_RESOLUTION),  # precision 7
        8: range(constants.GEO_HASH_PRECISION_8_RESOLUTION, constants.GEO_HASH_PRECISION_7_RESOLUTION),  # precision 8
        9: range(constants.GEO_HASH_PRECISION_9_RESOLUTION, constants.GEO_HASH_PRECISION_8_RESOLUTION),  # precision 9
        10: range(constants.GEO_HASH_PRECISION_10_RESOLUTION, constants.GEO_HASH_PRECISION_9_RESOLUTION),
        # precision 10
        11: range(0, constants.GEO_HASH_PRECISION_10_RESOLUTION)  # precision 11
    }

    # init: Initialize the PingGeoHash with a threshold and a fuser
    def __init__(self, threshold: float):
        self.geo_hash = {}
        self._precision = self.generate_precision(threshold)

    # precision: Return the precision of the geohash
    @property
    def precision(self) -> int:
        return self._precision

    # generate_precision: Generate the precision of the geohash based on the threshold
    def generate_precision(self, threshold: float) -> int:
        for i, rng in self.geo_hash_precisions.items():
            # force the floats to ints to match the ranges
            if math.floor(threshold) in rng:
                if i > 1:
                    return i - 1
        print("Error we should not be here: get_precision has a gap in the ranges or a giant threshold")
        return 1

    # put: Add a ping to the geohash or fuse it with an existing ping
    # it returns either a list of two pings if a match is found or a list of one ping if no match is found
    def put(self, ping: Ping) -> list[Ping]:
        geo_key = pgh.encode(ping.latitude, ping.longitude, precision=self._precision)
        if geo_key in self.geo_hash:
            match: list[Ping] = [copy(self.geo_hash[geo_key]), copy(ping)]
            self.geo_hash[geo_key] = self.geo_hash[geo_key].merge(ping)
            return match
        else:
            self.geo_hash[geo_key] = ping
            return [ping]

    def remove_duplicates(self, inputs: list[Ping]) -> list[Ping]:
        temp_hash: PingGeoHash = PingGeoHash(self._precision)
        for ping in inputs:
            temp_hash.put(ping)
        return list(temp_hash.geo_hash.values())

    def fuse(self, object_list: list[Ping]) -> tuple[list[tuple[Ping, Ping]], list[Ping]]:
        sanitized = self.remove_duplicates(object_list)
        matched: list[tuple[Ping, Ping]] = []
        unmatched: list[Ping] = []
        for obj in sanitized:
            res = self.put(obj)
            if len(res) > 1:
                matched.append((res[0], res[1]))
            else:
                unmatched.append(res[0])
        return matched, unmatched

    def get(self, uid: str) -> Ping | None:
        for ping in self.geo_hash.values():
            if ping.track_id == uid:
                return ping
        return None
