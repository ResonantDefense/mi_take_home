from abc import ABC, abstractmethod

from mypy.checker import TypeVar, Generic


class IdGenerator(ABC):
    """
     Abstract base class for generating unique identifiers.

     This class defines the interface that must be implemented by subclasses
     to provide a mechanism for generating unique identifiers. The type of
     identifiers (e.g., numeric, alphanumeric) is determined by the specific
     implementation of the subclass.

     Methods:
         generate_id: Abstract method that, when implemented, will generate
                      and return a unique identifier.
     """

    @abstractmethod
    def generate_id(self):
        """
        Generate and return a unique identifier.

        This method must be implemented by subclasses to define the specific
        strategy for generating unique identifiers. The nature and format of
        the generated identifier (e.g., integer, UUID, string) depend on the
        implementation.

        Returns:
            A unique identifier in the format defined by the subclass implementation.
        """
        pass


class TimeGenerator(ABC):
    """
    Abstract base class for generating time-related values.

    This class serves as an interface for subclasses that implement
    specific strategies for generating time-related values. These could
    range from simple timestamps to more complex time structures, depending
    on the needs of the application and the implementation details of the subclass.

    The primary purpose of this class is to ensure that all subclasses follow a
    consistent interface for time generation, making them easily interchangeable
    in the context of larger applications where time generation is a requirement.

    Methods:
        generate_time: Abstract method that must be implemented by subclasses to
                       define the specific mechanism for generating time values.
    """
    @abstractmethod
    def generate_time(self):
        pass


Point2d = tuple[float, float]
Point3d = tuple[float, float, float]
Point = TypeVar('Point', Point2d, Point3d)

T = TypeVar('T')


class DistanceCalculator(ABC):
    """
    Abstract base class for calculating the distance between two points.

    This class defines a common interface for distance calculation between
    two points, encapsulated by the `Point` class (or any class that represents
    a point in space). Subclasses are expected to implement the `calculate`
    method, providing specific algorithms for distance calculation, such as
    Euclidean, Manhattan, or any other metric.

    The class leverages polymorphism, allowing clients to use different distance
    calculation strategies interchangeably without changing the client code. It
    encapsulates the "strategy" pattern for distance calculation.

    Methods:
        calculate: Abstract method that must be implemented by subclasses to
                   calculate and return the distance between two points.
    """
    @abstractmethod
    def calculate(self, p1: Point, p2: Point) -> float:
        """
        Calculate and return the distance between two points.

        Parameters:
            p1 (Point): The first point in space.
            p2 (Point): The second point in space.

        Returns:
            float: The calculated distance between `p1` and `p2`, using the
                   specific strategy implemented by the subclass.

        The nature of the calculation (e.g., considering a 2D plane, 3D space,
        or even more abstract dimensions) and the distance metric (Euclidean,
        Manhattan, etc.) depend on the subclass implementation.
        """
        pass


class DistanceCalculator2d(ABC):
    """
    Abstract base class for calculating the distance between two points in 2D space.

    This class serves as an interface for subclasses that implement specific
    algorithms for calculating the distance between two points represented by
    the `Point2d` class. It defines the structure for distance calculation in
    a two-dimensional context, encouraging the implementation of various
    distance metrics (e.g., Euclidean, Manhattan) suitable for 2D spaces.

    Subclasses should provide concrete implementations of the `calculate` method,
    tailored to the specific requirements of their distance calculation logic.
    This approach allows for flexible distance computations within 2D spaces,
    facilitating easy integration and interchangeability of different calculation
    strategies in applications that operate in two dimensions.

    Methods:
        calculate: Abstract method to be implemented by subclasses for calculating
                   and returning the distance between two 2D points.
    """
    @abstractmethod
    def calculate(self, p1: Point2d, p2: Point2d) -> float:
        """
        Calculate and return the distance between two points in 2D space.

        Parameters:
            p1 (Point2d): The first point in 2D space.
            p2 (Point2d): The second point in 2D space.

        Returns:
            float: The calculated distance between `p1` and `p2` using the specific
                   strategy implemented by the subclass. This could be based on
                   different metrics suitable for 2D space, such as the Euclidean
                   or Manhattan distance.

        Implementations should consider the specific characteristics of 2D space
        to optimize the calculation and ensure accuracy and efficiency.
        """
        pass


class Tracker(ABC, Generic[T]):
    """
    Abstract base class for tracking objects of type T.

    This class defines a generic interface for tracking, updating, and
    managing a collection of objects of a specific type. It is designed
    to be subclassed with concrete implementations that define how objects
    are updated, how callsigns are assigned for identification, and how
    objects can be retrieved.

    Methods:
        update: Abstract method for updating tracked objects based on new inputs.
        set_callsign: Abstract method for assigning a unique callsign to an object.
        get: Abstract method for retrieving an object by its unique identifier.

    The class leverages generics, allowing it to be used with any type of object
    that needs tracking and management in a variety of applications.
    """
    @abstractmethod
    def update(self, inputs: list[T]) -> tuple[list[tuple[T, T]], list[T]]:
        """
        Update the tracker with a list of new inputs and return the matched and unmatched elements.

        Parameters:
            inputs (List[T]): A list of new inputs of type T to update the tracker with.

        Returns:
            Tuple[List[Tuple[T, T]], List[T]]: A tuple containing two elements:
                - A list of tuples, each consisting of a pair (previous state, new state)
                  representing the matched object pairs.
                - A list of unmatched objects.

        This method must be implemented by subclasses to specify how the tracker
        updates its state based on new inputs and how it tracks changes to its objects.
        """
        pass

    @abstractmethod
    def set_callsign(self, uid: str, callsign: str):
        """
        Assign a unique callsign to an object identified by a unique identifier (uid).

        Parameters:
            uid (str): The unique identifier of the object to assign the callsign to.
            callsign (str): The callsign to assign to the object.

        This method must be implemented by subclasses to specify how callsigns
        are assigned to objects for identification purposes.
        """
        pass

    @abstractmethod
    def get(self, uid: str) -> T | None:
        """
        Retrieve an object by its unique identifier (uid).

        Parameters:
            uid (str): The unique identifier of the object to retrieve.

        Returns:
            T | None: The object identified by uid if it exists in the tracker,
                      otherwise None.

        This method must be implemented by subclasses to specify how objects
        are retrieved from the tracker using their unique identifiers.
        """
        pass


class FusibleCollection(ABC, Generic[T]):
    """
    Abstract base class for a collection of objects of type T that can be fused together.

    This class defines a generic interface for managing a collection of objects,
    allowing for operations such as fusing objects together based on specific criteria,
    retrieving objects by unique identifiers, and adding new objects to the collection.
    It is designed to be subclassed with concrete implementations that define the
    specific logic for these operations.

    The fusion operation is a key feature of this class, allowing for the combination
    of objects in the collection in a meaningful way, according to the rules defined
    in the subclasses.

    Methods:
        fuse: Abstract method for fusing objects in the collection.
        get: Abstract method for retrieving an object by its unique identifier.
        put: Abstract method for adding a new object to the collection.
    """
    @abstractmethod
    def fuse(self, object_list: list[T]) -> tuple[list[tuple[T, T]], list[T]]:
        """
        Fuse objects in the given list together based on specific criteria.

        Parameters:
            object_list (List[T]): A list of objects of type T to be fused.

        Returns:
            Tuple[List[Tuple[T, T]], List[T]]: A tuple containing:
                - A list of tuples, each representing a pair of objects that were fused together.
                - A list of objects that were not fused.

        This method must be implemented by subclasses to specify the logic for fusing
        objects in the collection. The criteria and mechanism for fusion will depend on
        the subclass implementation.
        """
        pass

    @abstractmethod
    def get(self, uid: str) -> T | None:
        """
        Retrieve an object by its unique identifier (uid).

        Parameters:
            uid (str): The unique identifier of the object to retrieve.

        Returns:
            T | None: The object identified by uid if it exists in the collection,
                      otherwise None.

        This method must be implemented by subclasses to specify how objects
        are retrieved from the collection using their unique identifiers.
        """
        pass

    @abstractmethod
    def put(self, obj: T) -> list[T]:
        """
        Add a new object to the collection.

        Parameters:
            obj (T): The object to be added to the collection.

        Returns:
            List[T]: Contains either one or two elements depending on if it was matched
            with the existing collection or not.

        This method must be implemented by subclasses to specify the logic for
        adding new objects to the collection. Implementations should ensure the
        collection maintains its integrity and follows the rules defined for the
        specific type of collection being managed.
        """
        pass
