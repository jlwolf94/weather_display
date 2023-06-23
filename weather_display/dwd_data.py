"""
The dwd_data module contains the DwdData class that is used to make all calls
to the DWD-API and preprocess the retrieved data.
"""

from deutschland import dwd
from deutschland.dwd.api import default_api
from deutschland.dwd.model.station_overview_extended_get_station_ids_parameter_inner \
    import StationOverviewExtendedGetStationIdsParameterInner
from deutschland.dwd.model.station_overview import StationOverview
from deutschland.dwd.model.station_overview10865 import StationOverview10865
from deutschland.dwd.model.error import Error
from pprint import pprint


class DwdData:
    """
    Class that contains the DWD-API configuration, stores retrieved data and
    can preprocess the data. The class is initialized with the default API
    configuration and a station identifier.
    """

    def __init__(self, station_identifier):
        """
        Constructor for the DwdData objects.

        Parameters
        ----------
        station_identifier (str):
            Station identifier of an existing weather station.
        """

        # Defining the host is optional and defaults to https://app-prod-ws.warnwetter.de/v30
        # See configuration.py for a list of all supported configuration parameters.
        self.config = dwd.Configuration(host="https://app-prod-ws.warnwetter.de/v30")
        """
        config (Configuration):
            Configuration object with all settings for the DWD-API.
        """

        self.station_identifier = str(station_identifier)
        """
        station_identifier (str):
            Station identifier of an existing weather station.
        """

        self.error_state = False
        """
        error_state (bool):
            Current error state that indicates whether the last API call
            raised an error or not.
        """

        self.raw_data = None
        """
        raw_data (StationOverview):
            Raw data that is retrieved as a json file in the API response and
            converted to a StationOverview object.
        """

    def get_data(self):
        """
        Function that tries to retrieve new data for the saved station from the API.

        Returns
        -------
        success (bool):
            Indicates wheter the API call was a success or not.
        """

        # Enter a context with an instance of the API client.
        with dwd.ApiClient() as api_client:
            # Create an instance of the API class.
            api_instance = default_api.DefaultApi(api_client)

            # The stations_ids parameter uses the
            # StationOverviewExtendedGetStationIdsParameterInner class and the DWD
            # weather station identifier that can be found in the list on:
            # https://www.dwd.de/DE/leistungen/klimadatendeutschland/stationsliste.html
            station_ids = [
                StationOverviewExtendedGetStationIdsParameterInner(
                    station_ids=self.station_identifier),
            ]

            # Line 892 of the api_client.py needed to be modified to:
            # >>> param_value_full = (base_name, [d[param_name] for d in param_value])
            # Without the modification the response is empty.
            try:
                self.raw_data = api_instance.station_overview_extended_get(
                    station_ids=station_ids)

                # Check the content of the data response.
                if self.raw_data is None or not self.raw_data:
                    self.error_state = True
                    self.raw_data = None
                    print(f'No data could be retrieved for the '
                          f'station {self.station_identifier}')
                else:
                    self.error_state = False

            except dwd.ApiException as e:
                self.error_state = True
                self.raw_data = None
                print(f'Exception when calling DWD-API: {e}')

        return not self.error_state

    def print_raw_data(self):
        """
        Function that tries to print out the currently stored raw data.
        """

        if self.raw_data is None or not self.raw_data:
            print("There is no data that could be printed.")
        else:
            pprint(self.raw_data)

    def get_station_name(self):
        """
        Function that extracts the station name from the raw data.

        Returns
        -------
        station_name (str or None):
            The station name or None if it is not present.
        """

        if self.raw_data is None or not self.raw_data:
            return None
        else:
            return self.station_identifier

    def get_formatted_time(self):
        """
        Function that extracts the closest past time compared to the
        current time from the raw data and returns it formatted.

        Returns
        -------
        formatted_time (str):
            Formatted time as HH:MM.
        """

        return "None"

    def get_current_temperature(self):
        """
        Function that extracts and returns the current temperature for
        the closest time from the raw data.

        Returns
        -------
        temperature (float):
            Current temperature from the raw data.
        """

        return 0.0

    def test_print(self):
        """
        Function to test the formatted print.
        """

        station_name = "Test"
        formatted_time = "16:00"
        temperature = 23.1
        daily_min = 10.2
        daily_max = 30.2
        forecast = "sunny"
        print(f'Station: {station_name:30}    '
              f'Time: {formatted_time:19}    '
              f'Temperature: {temperature:.1f} °C')
        print(f'Daily forecast: {forecast:23}    '
              f'Daily min. temp.: {daily_min:.1f} °C    '
              f'Daily max. temp.: {daily_max:.1f} °C')
