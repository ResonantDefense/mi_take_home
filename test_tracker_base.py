from unittest import TestCase

from ping import Ping
from fusible_geo_hash import PingGeoHash
from fusible_nearest_neighbor import PingList
from tracker_base import TrackerBase


def generate_close_coordinate(ping: Ping):
    return Ping.Builder().build(ping.track_id, ping.latitude + 0.00001, ping.longitude + 0.00001)


def generate_far_coordinate(ping: Ping):
    return Ping.Builder().build(ping.track_id, ping.latitude + 0.1, ping.longitude + 0.1)


def print_matches(matches: list[tuple[Ping, Ping]]):
    for match in matches:
        print(f"Matched: {str(match[0])} and {str(match[1])}")


def print_unmatched(unmatched: list[Ping]):
    for ping in unmatched:
        print(f"Unmatched: {str(ping)}")


class TestTrackerBase(TestCase):
    """
    Tests for verifying the functionality of the TrackerBase class with different underlying storage mechanisms.
    """
    def setUp(self):
        """
        Setup common test fixtures.
        """
        self.threshold = 5.0
        self.base_ping = Ping.Builder().build("BasePing", 37.7749, 122.419451)

    def test_tracker_base_with_nearest_neighbor(self):
        """
        Tests the TrackerBase functionality using the nearest neighbor storage mechanism.
        """
        self.tracker_nn = TrackerBase(self.threshold, PingList(self.threshold))
        self._test_update_from_tracker(self.tracker_nn)

    def test_tracker_base_with_geo_hash(self):
        """
        Tests the TrackerBase functionality using the geo hash storage mechanism.
        """
        self.tracker_hash = TrackerBase(self.threshold, PingGeoHash(self.threshold))
        self._test_update_from_tracker(self.tracker_hash)

    def _test_update_from_tracker(self, tracker: TrackerBase):
        """
        Helper method to test updating tracker with various ping configurations.
        """
        # Test with all the same ping
        ping_list = [self.base_ping, self.base_ping, self.base_ping]
        matched, unmatched = tracker.update(ping_list)
        self.assertEqual(0, len(matched), "Expected no matched pings with identical inputs.")
        self.assertEqual(1, len(unmatched), "Expected a single unmatched ping with identical inputs.")

        # Test with all different pings
        far_pings = [self.base_ping]
        for _ in range(1, 10):
            far_pings.append(generate_far_coordinate(far_pings[-1]))
        matched, unmatched = tracker.update(far_pings)
        self.assertEqual(1, len(matched), "Expected 1 match with original base ping. The rest are too far apart")
        self.assertEqual(9, len(unmatched), "Expected all pings to be unmatched except the 1 orignal base pings.")

        # Test re-updating tracker with the same pings
        matched, unmatched = tracker.update(far_pings)
        self.assertEqual(len(far_pings), len(matched),
                         "Expected all pings to match when re-updating with the same inputs.")
        self.assertEqual(0, len(unmatched), "Expected no unmatched pings when re-updating with the same inputs.")

    def test_get_and_set_callsign(self):
        """
        Tests getting a ping by ID and setting a new callsign for a ping.
        """
        tracker = TrackerBase(5.0, PingList(5.0))
        tracker.update([self.base_ping])

        expected_callsign = "NewCallsign"
        tracker.set_callsign(self.base_ping.track_id, expected_callsign)
        updated_ping = tracker.get(self.base_ping.track_id)

        self.assertIsNotNone(updated_ping, "Expected to retrieve a ping by track_id.")
        self.assertEqual(expected_callsign, updated_ping.callsign, "Expected the callsign to be updated.")
