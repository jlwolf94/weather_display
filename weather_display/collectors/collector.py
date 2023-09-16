"""
The collector module contains the Collector class that bundles and initializes
the different data sources. The collector provides methods to gather and
update data contained in the different data sources.
"""

from weather_display.models.station import Station
from weather_display.models.display_data import DisplayData
from weather_display.collectors.data_dwd import DataDWD
from weather_display.collectors.data_w24 import DataW24
from weather_display.collectors.data_won import DataWon


class Collector:
    """
    The Collector class provides methods to gather and update
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
        Constructor for the Collector objects.

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

        # Initialize the data sources.
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

    @staticmethod
    def combine_display_data(dd_res, dd_new):
        """
        Method that updates the result DisplayData object with new data of
        the new DisplayData object if it does not match the default data
        in a default DisplayData object.

        Parameters
        ----------
        dd_res (DisplayData):
            DisplayData object with the current result data.

        dd_new (DisplayData):
            DisplayData object with the new data.

        Returns
        -------
        dd_res (DisplayData):
            The updated result DisplayData object.
        """

        # Get default DisplayData object for comparison.
        dd_def = DisplayData()

        if (dd_new.station_name != dd_def.station_name
            and dd_new.station_name != dd_res.station_name):
            dd_res.station_name = dd_new.station_name

        if (dd_new.date_time is not None
            and dd_new.date_time >= dd_res.date_time):
            dd_res.date_time = dd_new.date_time
            dd_res.temperature = dd_new.temperature
            dd_res.dew_point = dd_new.dew_point
            if (dd_new.precipitation != dd_def.precipitation):
                dd_res.precipitation = dd_new.precipitation

        if (dd_new.forecast != dd_def.forecast
            and dd_new.forecast != dd_res.forecast):
            dd_res.forecast = dd_new.forecast
            dd_res.daily_min = dd_new.daily_min
            dd_res.daily_max = dd_new.daily_max

        return dd_res

    def get_display_data(self):
        """
        Method that gets the weather data that will be displayed from
        the different data sources. The combined data of all data sources
        is returned in a new DisplayData object.

        Returns
        -------
        display_data (DisplayData):
            A DisplayData object containing all weather data from all
            data sources formatted for display purposes.
        """

        # Check whether an update of the data is necessary.
        if not self.is_updated:
            self.update()

        # Combine the weather data in a result DisplayData object.
        dd_res = DisplayData()
        is_first = True
        for data in self.data_sources.values():
            if is_first:
                dd_res = data.get_display_data()
                is_first = False
            else:
                dd_res = self.combine_display_data(dd_res, data.get_display_data())

        # Reset the update status and return the result data.
        self.is_updated = False
        return dd_res

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
