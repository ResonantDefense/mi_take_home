from unittest import TestCase

from ping import Ping


class Test(TestCase):
    """
    Unit tests for the `Ping` class.

    This test suite focuses on verifying the behavior of key functionalities within the Ping class,
    specifically testing methods that determine the earliest and newest pings based on their start and observation times,
    and the ability to correctly merge two Ping instances into a single, updated Ping instance.
    """
    def test_get_earliest(self):
        """
        Tests whether the `get_earliest` method correctly identifies the Ping instance
        with the earliest start time when compared with another Ping instance.
        """
        ping1 = Ping("1", "A", 1, 1, 1, 1)
        ping2 = Ping("2", "B", 2, 2, 2, 2)
        self.assertEqual(ping1.get_earliest(ping2), ping1)

    def test_get_newest(self):
        """
        Tests the `get_newest` method to ensure it accurately identifies the Ping instance
        with the most recent observation time when compared with another Ping instance.
        """
        ping1 = Ping("1", "A", 1, 1, 1, 1)
        ping2 = Ping("2", "B", 2, 2, 2, 2)
        self.assertEqual(ping1.get_newest(ping2), ping2)

    def test_merge(self):
        """
        Tests the `merge` method to ensure that two Ping instances can be merged correctly,
        preserving the original track_id and callsign, while updating the observation time,
        latitude, and longitude based on the newest Ping.
        """
        ping1 = Ping("8655725a", "VESSEL1", 1, 9, 74.1200002, 33.4500007)
        ping2 = Ping("99c1bcc7", "TARGET1", 2, 10, 74.1200003, 33.4500006)
        merged_ping = ping1.merge(ping2)
        self.assertEqual(merged_ping.track_id, "8655725a", "track_id was changed")
        self.assertEqual(merged_ping.callsign, "VESSEL1", "callsign was changed")
        self.assertEqual(merged_ping.observation_time, 10, "observation_time has not but updated")
        self.assertEqual(merged_ping.latitude, 74.1200003, "latitude was changed")
        self.assertEqual(merged_ping.longitude, 33.4500006, "longitude was changed")
