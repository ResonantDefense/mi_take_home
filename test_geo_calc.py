import timeit
from unittest import TestCase

from geo_calc import geodesic_distance, euclidean_distance, great_circle_distance


def find_distance_difference_threshold(lat1, lon1, distance_func1, distance_func2, start_lat, start_lon,
                                       increment=0.0000001, threshold=1.0):
    lat2, lon2 = start_lat, start_lon
    while True:
        dist1 = distance_func1((lat1, lon1), (lat2, lon2))
        dist2 = distance_func2((lat1, lon1), (lat2, lon2))
        if abs(dist1 - dist2) > threshold:
            return geodesic_distance((lat1, lon1), (lat2, lon2))
        lat2 += increment
        lon2 += increment


class Test(TestCase):
    def test_geodesic_distance(self):
        p1 = (37.7749, 122.4194)
        p2 = (37.7748, 122.4195)
        dist = round(geodesic_distance(p1, p2), 2)
        self.assertEqual(dist, 14.17)

    def test_euclidean_distance(self):
        p1 = (37.7749, 122.4194)
        p2 = (37.7749, 122.41941)
        dist = round(euclidean_distance(p1, p2))
        self.assertEqual(dist, 1)

    def test_great_circle_distance(self):
        p1 = (37.7749, 122.4194)
        p2 = (37.7748, 122.4195)
        dist = round(great_circle_distance(p1, p2), 2)
        self.assertEqual(dist, 14.17)

    def test_benchmarks(self):
        euclidean_bench = timeit.timeit("euclidean_distance((37.7749, 122.41945), (37.7749, 122.41945))",
                                        setup="from geo_calc import euclidean_distance", number=100000)
        geodesic_bench = timeit.timeit("geodesic_distance((37.7749, 122.41945), (37.7749, 122.41945))",
                                       setup="from geo_calc import geodesic_distance", number=100000)
        cirle_bench = timeit.timeit("great_circle_distance((37.7749, 122.41945), (37.7749, 122.41945))",
                                    setup="from geo_calc import great_circle_distance", number=100000)
        print(f"Euclidean Time to execute 100,000: {euclidean_bench}")
        print(f"Geodesic Time to execute 100,000: {geodesic_bench}")
        print(f"Circle Time to execute 100,000: {cirle_bench}")

    def test_divergence(self):
        print(
            f"Divergence Beyond 1 meter for Euclidean={find_distance_difference_threshold(37.7749, 122.41945, euclidean_distance, geodesic_distance,
                                                                                          37.7749,
                                                                                          122.41945)} meters")
        print(
            f"Divergence Beyond 1 meter for Great Circle={find_distance_difference_threshold(37.7749, 122.41945, great_circle_distance, geodesic_distance,
                                                                                             37.7749,
                                                                                             122.41945)} meters")
