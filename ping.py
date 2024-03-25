import time
import uuid

from abstract import IdGenerator, TimeGenerator


class Ping:
    """
    Represents a tracking ping with spatial and temporal data.

    Attributes:
        _track_id (str): Unique identifier for the tracking object.
        callsign (str): Callsign associated with the tracking object.
        _start_time (int): Start time of the tracking, typically representing when tracking began.
        observation_time (int): Time of the observation, indicating the latest update.
        latitude (float): Latitude of the tracking object.
        longitude (float): Longitude of the tracking object.
    """
    _track_id: str
    callsign: str
    _start_time: int
    observation_time: int
    latitude: float
    longitude: float

    def __init__(self, _track_id: str, callsign: str, start_time: int, observation_time: int, latitude: float,
                 longitude: float):
        """
        Initializes a new Ping instance.

        Parameters:
            _track_id (str): The unique identifier for the tracking object.
            callsign (str): The callsign associated with the tracking object.
            start_time (int): The start time of tracking.
            observation_time (int): The observation time for the latest update.
            latitude (float): The latitude of the tracking object.
            longitude (float): The longitude of the tracking object.
        """
        self._track_id = _track_id
        self.callsign = callsign
        self._start_time = start_time
        self.observation_time = observation_time
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return f"Track ID: {self._track_id}, Callsign: {self.callsign}, Start Time: {self._start_time}, Observation Time: {self.observation_time}, Latitude: {self.latitude}, Longitude: {self.longitude}"

    @property
    def track_id(self) -> str:
        return self._track_id

    @property
    def start_time(self) -> int:
        return self._start_time

    def merge(self, other: 'Ping') -> 'Ping':
        """
        Merges this Ping with another Ping, combining temporal and spatial data.

        The merged Ping uses the earliest start time, the most recent observation time,
        and the location of the newest Ping.

        Parameters:
            other (Ping): Another Ping instance to merge with.

        Returns:
            Ping: A new Ping instance resulting from the merge.
        """
        earliest = self.get_earliest(other)
        newest = self.get_newest(other)
        return Ping(
            _track_id=earliest._track_id,
            callsign=earliest.callsign,
            start_time=earliest._start_time,
            observation_time=newest.observation_time,
            latitude=newest.latitude,
            longitude=newest.longitude
        )

    def get_earliest(self, other: 'Ping') -> 'Ping':
        if self._start_time < other._start_time:
            return self
        else:
            return other

    def get_newest(self, other: 'Ping') -> 'Ping':
        if self.observation_time > other.observation_time:
            return self
        else:
            return other

    class Builder:
        """
        Builder class for constructing Ping objects.

        Provides a fluent interface for setting up and creating new Ping instances
        with customized ID and time generation strategies.
        """
        _id_generator: IdGenerator
        _time_generator: TimeGenerator

        def __init__(self):
            self._id_generator = LocalIdInitializer()
            self._time_generator = LocalTimeInitializer()

        # with_id_generator method: set the id_generator method
        def with_id_generator(self, id_generator: IdGenerator) -> 'Ping.Builder':
            """
            Sets the ID generator for the Ping being built.

            Parameters:
                id_generator (IdGenerator): The ID generator to use.

            Returns:
                Ping.Builder: The Builder instance for chaining.
            """
            self._id_generator = id_generator
            return self

        def with_time_generator(self, time_generator: TimeGenerator) -> 'Ping.Builder':
            """
            Sets the time generator for the Ping being built.

            Parameters:
                time_generator (TimeGenerator): The time generator to use.

            Returns:
                Ping.Builder: The Builder instance for chaining.
            """
            self._time_generator = time_generator
            return self

        def build(self, callsign: str, latitude: float, longitude: float) -> 'Ping':
            """
            Constructs a new Ping instance using the configured ID and time generators.

            Parameters:
                callsign (str): The callsign to associate with the Ping.
                latitude (float): The latitude of the Ping's location.
                longitude (float): The longitude of the Ping's location.

                Returns:
                    Ping: A new Ping instance with the generated ID and times.
            """
            return Ping(
                _track_id=self._id_generator.generate_id(),
                callsign=callsign,
                start_time=self._time_generator.generate_time(),
                observation_time=self._time_generator.generate_time(),
                latitude=latitude,
                longitude=longitude
            )


class LocalIdInitializer(IdGenerator):
    def generate_id(self) -> str:
        return str(uuid.uuid4())


class LocalTimeInitializer(TimeGenerator):
    def generate_time(self) -> int:
        return int(time.time() * 1000)
