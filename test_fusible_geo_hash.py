"""
Unit Tests for the PingGeoHash Class

This module contains unit tests for the PingGeoHash class, which is responsible for managing a collection of Ping objects and providing functionality to fuse them based on geographic proximity. The tests cover various scenarios including fusing identical pings, handling distinct pings located far apart, re-fusing the same set of pings, and removing duplicate pings from a list.

Each test case is designed to verify the correctness of the PingGeoHash's methods under different conditions, ensuring that pings are appropriately fused or identified as unique based on their geographic coordinates and the specified threshold for proximity.

Setup:
- The Ping and PingGeoHash classes, along with any required dependencies (e.g., Geo2dDistanceCalculator), must be available.
- Helper functions such as generate_far_coordinate are assumed to be defined elsewhere in the test suite or the application code.

Usage:
- Run this module directly using a unittest-compatible test runner (e.g., `python -m unittest this_module.py`).
- Alternatively, it can be included as part of a larger test suite and run using a test runner that supports unittest discovery.
"""

from unittest import TestCase

from ping import Ping
from test_tracker_base import generate_far_coordinate, generate_close_coordinate
from fusible_geo_hash import PingGeoHash


class Test(TestCase):

    def setUp(self):
        self.threshold = 5.0
        self.base_ping = Ping.Builder().build("BasePing", 37.7749, -122.4194)
        self.geo_hash = PingGeoHash(self.threshold)

    def test_fuse_with_identical_pings(self):
        ping_list = [self.base_ping for _ in range(3)]
        ghash = PingGeoHash(self.threshold)
        matched, unmatched = ghash.fuse(ping_list)
        self.assertEqual(0, len(matched), "Expected no matched pings when all are identical.")
        self.assertEqual(1, len(unmatched), "Expected a single unmatched ping when all are identical.")

    def test_fuse_with_distinct_far_pings(self):
        # Assuming generate_far_coordinate is a function that generates pings far from each other
        far_pings = [self.base_ping]
        for _ in range(1, 10):
            far_pings.append(generate_far_coordinate(far_pings[-1]))
        ghash = PingGeoHash(self.threshold)
        matched, unmatched = ghash.fuse(far_pings)
        self.assertEqual(0, len(matched), "Expected no matched pings when all are far apart.")
        self.assertEqual(10, len(unmatched), "Expected all pings to be unmatched when all are far apart.")

    def test_fuse_repeated_with_same_pings(self):
        far_pings = [self.base_ping]
        for _ in range(1, 10):
            far_pings.append(generate_far_coordinate(far_pings[-1]))
        self.geo_hash.fuse(far_pings)  # First fusion to populate the geo_hash
        matched, unmatched = self.geo_hash.fuse(far_pings)  # Fuse the same pings again
        self.assertEqual(10, len(matched), "Expected all pings to match when the same set is fused again.")
        self.assertEqual(0, len(unmatched), "Expected no unmatched pings when the same set is fused again.")

    def test_fuse_close_pings(self):
        close_pings = [Ping.Builder().build("ClosePing", 37.2783, -122.5432)]
        for _ in range(1, 2):
            close_pings.append(generate_close_coordinate(close_pings[-1]))
        matched, unmatched = self.geo_hash.fuse(close_pings)
        self.assertEqual(0, len(matched), "Expected close pings to converge.")
        self.assertEqual(1, len(unmatched), "Expected 1 unmatched converged.")

    def test_remove_duplicates_with_identical_pings(self):
        # Assuming each call to Ping.Builder().build generates a unique Ping object
        identical_pings = [Ping.Builder().build("N12345", 37.7749, -122.4194) for _ in range(6)]
        unique_pings = self.geo_hash.remove_duplicates(identical_pings)
        self.assertEqual(1, len(unique_pings), "Expected duplicates to be removed, leaving one unique ping.")
