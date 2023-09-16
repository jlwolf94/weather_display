"""
The collectors controller module contains the CollectorsController class that bundles
and initializes the different data sources. The Controller provides methods to
gather and update data contained in the different data sources.
"""

from weather_display.models.station import Station
from weather_display.collectors.data_dwd import DataDWD
from weather_display.collectors.data_w24 import DataW24
from weather_display.collectors.data_won import DataWon


class CollectorsController:
    """
    The CollectorsController class provides methods to gather and update
    data contained in the different data sources. It can initialize all
    data sources or only some selected sources.
    """

    SOURCES = ("dwd", "w24", "won")
    """
    SOURCES (tuple[str, str, str]):
        A tuple containing the names of available data sources.
    """

    def __init__(self, stations):
        """
        Constructor for the CollectorsController objects.

        Parameters
        ----------
        stations (Optional[dict[str, Station]]):
            A dictionary containing the different stations used for the
            initialization of the data sources labeled with the associated
            data source name.
        """

        self.data_sources = {}
        """
        data_sources (dict[str, Data]):
            A dictionary containing the initialized data sources labeled
            with the associated data source name. Default value is the empty
            dictionary.
        """

        self.is_updated = False
        """
        is_updated (bool):
            Combined status of the last update method calls.
            Default value is False.
        """

        if stations is None or not stations:
            # Set a default station for the default data source.
            self.data_sources.update({self.SOURCES[0]: DataDWD(Station())})
        else:
            # Iterate the dictionary and initialize the found sources.
            for source, station in stations.items():
                if source == self.SOURCES[1]:
                    self.data_sources.update({self.SOURCES[1]: DataW24(station)})
                elif source == self.SOURCES[2]:
                    self.data_sources.update({self.SOURCES[2]: DataWon(station)})
                else:
                    self.data_sources.update({self.SOURCES[0]: DataDWD(station)})

    def update(self):
        """
        Method that updates the station_data of all data sources by calling
        the associated update method of the sources. It also saves the combined
        success status of the updates.
        """

        # Call all update methods and combine the success status.
        is_updated = True
        for data in self.data_sources.values():
            is_updated = is_updated and data.update()

        self.is_updated = is_updated
