"""
The station module contains the station class that holds all informations
of a weather station.
"""


class Station:
    """
    Class that contains all informations of a weather station.
    """

    def __init__(self, name, number=0, type="", identifier="", latitude=0.0,
                 longitude=0.0, altitude=0, river_basin="", state="",
                 start=None, end=None):
        """
        Constructor for the Station objects.

        Parameters
        ----------
        name (str):
            Name of the station.

        number (int):
            Number of the station. Default value is 0.

        type (str):
            Type of the station. Default value is the empty string.

        identifier (str):
            Identifier of the station. Default value is the empty string.

        latitude (float):
            Latitude of the station. Default value is 0.0.

        longitude (float):
            Longitude of the station. Default value is 0.0.

        altitude (int):
            Altitude of the station in meters over normal zero.
            Default value is 0.

        river_basin (str):
            River basin near the station. Default value is the empty string.

        state (str):
            State in which the station stands. Default value is the empty string.

        start (Optional[datetime]):
            The start date of the data set. Default value is None.

        end (Optional[datetime]):
            The end date of the data set. Default value is None.
        """

        self.name = name
        """
        name (str):
            Name of the station.
        """

        self.number = number
        """
        number (int):
            Number of the station.
        """

        self.type = type
        """
        type (str):
            Type of the station.
        """

        self.identifier = identifier
        """
        identifier (str):
            Identifier of the station.
        """

        self.latitude = latitude
        """
        latitude (float):
            Latitude of the station.
        """

        self.longitude = longitude
        """
        longitude (float):
            Longitude of the station.
        """

        self.altitude = altitude
        """
        altitude (int):
            Altitude of the station in meter over normal zero.
        """

        self.river_basin = river_basin
        """
        river_basin (str):
            River basin near the station.
        """

        self.state = state
        """
        state (str):
            State in which the station stands.
        """

        self.start = start
        """
        start (Optional[datetime]):
            The start date of the data set.
        """

        self.end = end
        """
        end (Optional[datetime]):
            The end date of the data set.
        """
