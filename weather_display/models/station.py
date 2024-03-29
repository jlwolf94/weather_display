"""
The station module contains the station class that holds all information
of a weather station.
"""


class Station:
    """
    Class that contains all information of a weather station.
    """

    def __init__(
        self,
        name="Error",
        number=0,
        type="",
        identifier="0",
        latitude=0.0,
        longitude=0.0,
        altitude=0,
        river_basin="",
        state="",
        start=None,
        end=None,
    ):
        """
        Constructor for the Station objects.

        Args:
            name (str): Name of the station.
                Default name is Error.
            number (int): Number of the station.
                Default value is 0.
            type (str): Type of the station.
                Default value is the empty string.
            identifier (str): Identifier of the station.
                Default value is the empty string.
            latitude (float): Latitude of the station.
                Default value is 0.0.
            longitude (float): Longitude of the station.
                Default value is 0.0.
            altitude (int): Altitude of the station in meters over normal zero.
                Default value is 0.
            river_basin (str): River basin near the station.
                Default value is the empty string.
            state (str): State in which the station stands.
                Default value is the empty string.
            start (datetime, optional): The start date of the data set.
                Default value is None.
            end (datetime, optional): The end date of the data set.
                Default value is None.
        """

        self.name = name
        """
        str: Name of the station.
        """

        self.number = number
        """
        int: Number of the station.
        """

        self.type = type
        """
        str: Type of the station.
        """

        self.identifier = identifier
        """
        str: Identifier of the station.
        """

        self.latitude = latitude
        """
        float: Latitude of the station.
        """

        self.longitude = longitude
        """
        float: Longitude of the station.
        """

        self.altitude = altitude
        """
        int: Altitude of the station in meter over normal zero.
        """

        self.river_basin = river_basin
        """
        str: River basin near the station.
        """

        self.state = state
        """
        str: State in which the station stands.
        """

        self.start = start
        """
        datetime, optional: The start date of the data set.
        """

        self.end = end
        """
        datetime, optional: The end date of the data set.
        """
