from unittest import TestCase

from ping import Ping
from test_tracker_base import generate_far_coordinate, generate_close_coordinate
from fusible_nearest_neighbor import PingList


class Test(TestCase):
    """
    Unit tests for the PingList class focusing on fusion and duplication removal functionalities.

    These tests verify the PingList class's ability to correctly fuse together pings based on
    geographic proximity, handling cases of identical pings, pings that are far apart, and
    close pings, as well as its ability to remove duplicate pings from a collection.

    Attributes:
        threshold (float): The distance threshold used for determining whether pings are close enough to be fused.
        base_ping (Ping): A base Ping object used for creating test scenarios.
        nearest_neighbor (PingList): An instance of PingList used for testing fusion and duplication removal.
    """
    def setUp(self):
        self.threshold = 5.0
        self.base_ping = Ping.Builder().build("BasePing", 37.7749, -122.4194)
        self.nearest_neighbor = PingList(self.threshold)

    def test_fuse_with_identical_pings(self):
        """
        Test fusion with a list of identical pings.

        Verifies that when identical pings are fused, only one unique ping remains, with no matched pairs.
        """
        ping_list = [self.base_ping for _ in range(3)]
        nn = PingList(self.threshold)
        matched, unmatched = nn.fuse(ping_list)
        self.assertEqual(0, len(matched), "Expected no matched pings when all are identical.")
        self.assertEqual(1, len(unmatched), "Expected a single unmatched ping when all are identical.")

    def test_fuse_with_distinct_far_pings(self):
        """
        Test fusion with a list of pings that are far apart.

        Verifies that when pings are too far apart to be considered for fusion, all remain unmatched with no pairs formed.
        """
        far_pings = [self.base_ping]
        for _ in range(1, 10):
            far_pings.append(generate_far_coordinate(far_pings[-1]))
        nn = PingList(self.threshold)
        matched, unmatched = nn.fuse(far_pings)
        self.assertEqual(0, len(matched), "Expected no matched pings when all are far apart.")
        self.assertEqual(10, len(unmatched), "Expected all pings to be unmatched when all are far apart.")

    def test_fuse_repeated_with_same_pings(self):
        """
        Test re-fusing a list of previously fused pings.

        Ensures that pings previously added to the PingList and fused again are all recognized as matched,
        with none remaining unmatched.
        """
        far_pings = [self.base_ping]
        for _ in range(1, 10):
            far_pings.append(generate_far_coordinate(far_pings[-1]))
        self.nearest_neighbor.fuse(far_pings)  # First fusion to populate the geo_hash
        matched, unmatched = self.nearest_neighbor.fuse(far_pings)  # Fuse the same pings again
        self.assertEqual(10, len(matched), "Expected all pings to match when the same set is fused again.")
        self.assertEqual(0, len(unmatched), "Expected no unmatched pings when the same set is fused again.")

    def test_fuse_close_pings(self):
        """
        Test fusion with a list of close pings.

        Verifies that close pings, when fused, result in a single unmatched ping, with the others being considered duplicates.
        """
        close_pings = [Ping.Builder().build("ClosePing", 37.2783, -122.5432)]
        for _ in range(1, 2):
            close_pings.append(generate_close_coordinate(close_pings[-1]))
        matched, unmatched = self.nearest_neighbor.fuse(close_pings)
        self.assertEqual(0, len(matched), "Expected close pings to converge.")
        self.assertEqual(1, len(unmatched), "Expected 1 unmatched converged.")

    def test_remove_duplicates_with_identical_pings(self):
        """
        Test removal of duplicate pings.

        Verifies that when a list containing identical pings is processed to remove duplicates,
        only one unique ping remains.
        """
        identical_pings = [Ping.Builder().build("N12345", 37.7749, -122.4194) for _ in range(6)]
        unique_pings = self.nearest_neighbor.remove_duplicates(identical_pings)
        self.assertEqual(1, len(unique_pings), "Expected duplicates to be removed, leaving one unique ping.")

