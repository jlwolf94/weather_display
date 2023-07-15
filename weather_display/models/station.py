"""
The station module contains the station class that holds all informations
of a weather station.
"""


class Station:
    """
    Class that contains all informations of a weather station.
    """

    def __init__(self, name, number, type, identifier, latitude, longitude,
                 altitude, river_basin, state, start, end):
        """
        Constructor for the Station objects.

        Parameters
        ----------
        name (str):
            Name of the station.

        number (int):
            Number of the station.

        type (str):
            Type of the station.

        identifier (str):
            Identifier of the station.

        latitude (float):
            Latitude of the station.

        longitude (float):
            Longitude of the station.

        altitude (int):
            Altitude of the station in meter over normal zero.

        river_basin (str):
            River basin near the station.

        state (str):
            State in which the station stands.

        start (datetime):
            The start date of the data set.

        end (datetime):
            The end date of the data set.
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
        start (datetime):
            The start date of the data set.
        """

        self.end = end
        """
        end (datetime):
            The end date of the data set.
        """
