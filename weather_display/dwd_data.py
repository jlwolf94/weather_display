"""
The dwd_data module contains the DwdData class that is used to make all calls
to the DWD-API and preprocess the retrieved data.
"""

import datetime
import requests

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

        self.url = "https://app-prod-ws.warnwetter.de/v30"
        """
        url (str):
            Standard base url for the DWD-API.
        """

        self.attempts = 3
        """
        attempts (int):
            Number of connection attempts. Default value is 3.
        """

        self.timeout = 10
        """
        timeout (int):
            Connection timeout for a server answer in seconds.
            Default value is 10 seconds.
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

    def get_station_data(self, station_info):
        """
        Method that retrieves the current weather data for a station specified by
        its informations from the DWD-API. The recieved data is return in form
        of a deserialized json file.

        Parameters
        ----------
        station_info (dict):
            A dictionary containing all informations of the station.

        Returns
        -------
        station_data (dict):
            A dictionary containing all current weather data from the
            station specified by the station_info. An empty dictionary
            is returned if their is no data.
        """

        # Add url for a station data get request to the base url.
        url = self.url + "/stationOverviewExtended"

        # Build the parameters and the headers for the get request.
        params = {"stationIds": station_info.get("Stations-kennung", "0")}
        headers = {"accept": "application/json"}

        # Try to reach the server multiple times and handle occuring exceptions.
        for i in range(self.attempts):
            try:
                response = requests.get(url, params=params,
                                        headers=headers, timeout=self.timeout)
                response.raise_for_status()
            except requests.exceptions.HTTPError as err_http:
                print("HTTP Error:", err_http)
            except requests.exceptions.ConnectionError as err_con:
                print("Connection Error:", err_con)
            except requests.exceptions.Timeout as err_time:
                print("Timeout Error:", err_time)
            except requests.exceptions.TooManyRedirects as err_red:
                print("Redirect Error:", err_red)
            except requests.exceptions.RequestException as err_req:
                print("Request Error:", err_req)
            else:
                return response.json()

        return {}

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

    @staticmethod
    def get_display_data(station_info, station_data):
        """
        Method that extracts the weather data that will be displayed for
        the station specified by station_info from the provided station_data.
        The formatted data used for display is returned in a new dictionary.

        Parameters
        ----------
        station_info (dict):
            A dictionary containing all informations of the station.

        station_data (dict):
            A dictionary containing all current weather data from the
            station specified by the station_info.

        Returns
        -------
        display_data (dict):
            A dictionary containing all weather data for the given station
            formatted for display purposes.
        """

        # Extract the station identifier and name.
        stationId = station_info.get("Stations-kennung", "0")
        station_name = station_info.get("Stationsname", "Error")

        # Check whether forecast data is available.
        forecast_dict = station_data.get(stationId, {}).get("forecast1", {})
        if not forecast_dict:
            # Error values for time and temperature.
            formatted_time = "--:--"
            temperature = float("nan")
        else:
            # Extract start date and date step.
            start_date = datetime.datetime.fromtimestamp(forecast_dict["start"] / 1000)
            date_step = datetime.timedelta(milliseconds=forecast_dict["timeStep"])

            # Process the temperature list by adding the time to each temperature.
            date_temp_list = []
            for step, temp in enumerate(forecast_dict["temperature"]):
                if temp < -999 or temp > 999:
                    date_temp_list.append((start_date + (step * date_step), float("nan")))
                else:
                    date_temp_list.append((start_date + (step * date_step), temp / 10))

            # Find the date closest to the current date.
            curr_date = datetime.datetime.now()
            date_temp = min([dt for dt in date_temp_list if dt[0] <= curr_date],
                            key=lambda t: abs(curr_date - t[0]))

            formatted_time = date_temp[0].strftime("%H:%M")
            temperature = date_temp[1]

        # Check whether days data is available.
        days_list = station_data.get(stationId, {}).get("days", [])
        if not days_list:
            forecast = "Error"
            daily_min = float("nan")
            daily_max = float("nan")
        else:
            # Find the date in days list closest to the current date.
            curr_date = datetime.datetime.now()
            day = min([da for da in days_list
                       if datetime.datetime.strptime(da["dayDate"], "%Y-%m-%d") <= curr_date],
                      key=lambda d: abs(curr_date -
                                        datetime.datetime.strptime(d["dayDate"], "%Y-%m-%d")))

            icon_dict = {1: "sun", 2: "sun, slightly cloudy", 3: "sun, cloudy", 4: "clouds",
                         5: "fog", 6: "fog, risk of slipping", 7: "light rain", 8: "rain",
                         9: "heavy rain", 10: "light rain, risk of slipping",
                         11: "heavy rain, risk of slipping", 12: "rain, sporadic snowfall",
                         13: "rain, increased snowfall", 14: "light snowfall", 15: "snowfall",
                         16: "heavy snowfall", 17: "clouds, hail", 18: "sun, light rain",
                         19: "sun, heavy rain", 20: "sun, rain, sporadic snowfall",
                         21: "sun, rain, increased snowfall", 22: "sun, sporadic snowfall",
                         23: "sun, increased snowfall", 24: "sun, hail", 25: "sun, heavy hail",
                         26: "thunderstorm", 27: "thunderstorm, rain",
                         28: "thunderstorm, heavy rain", 29: "thunderstorm, hail",
                         30: "thunderstorm, heavy hail", 31: "wind"
                        }

            forecast = icon_dict.get(day["icon"], "Error")

            if day["temperatureMin"] < -999 or day["temperatureMin"] > 999:
                daily_min = float("nan")
            else:
                daily_min = day["temperatureMin"] / 10

            if day["temperatureMax"] < -999 or day["temperatureMax"] > 999:
                daily_max = float("nan")
            else:
                daily_max = day["temperatureMax"] / 10

        # Return all gathered data in a dictionary.
        return {"station_name": station_name,
                "formatted_time": formatted_time,
                "temperature": temperature,
                "forecast": forecast,
                "daily_min": daily_min,
                "daily_max": daily_max
               }

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
              f'Temperature: {temperature:5.1F} °C')
        print(f'Daily forecast: {forecast:23}    '
              f'Daily min. temp.: {daily_min:5.1F} °C    '
              f'Daily max. temp.: {daily_max:5.1F} °C')
