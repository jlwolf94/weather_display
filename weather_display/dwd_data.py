"""
The dwd_data module contains the DwdData class that is used to make all direct calls
to the DWD-API, save the received data and preprocess the received data for display
purposes.
"""

import datetime
import requests

from weather_display.display_data import DisplayData


class DwdData:
    """
    Class that contains the DWD-API base url, stores the station name and informations
    used for the data requests. It stores the received data for later use or display.
    """

    def __init__(self, station_name, station_info, attempts=3, timeout=10):
        """
        Constructor for the DwdData objects.

        Parameters
        ----------
        station_name (str):
            Name of the station.

        station_info (dict):
            A dictionary containing the informations of the station.

        attempts (int):
            Number of connection attempts. Default value is 3.

        timeout (int):
            Connection timeout for a server answer in seconds.
            Default value is 10 seconds.
        """

        self.station_name = station_name
        """
        station_name (str):
            Name of the station.
        """

        self.station_info = station_info
        """
        station_info (dict):
            A dictionary containing the informations of the station.
        """

        self.url = "https://app-prod-ws.warnwetter.de/v30"
        """
        url (str):
            Standard base url for the DWD-API.
        """

        self.attempts = attempts
        """
        attempts (int):
            Number of connection attempts. Default value is 3.
        """

        self.timeout = timeout
        """
        timeout (int):
            Connection timeout for a server answer in seconds.
            Default value is 10 seconds.
        """

        self.station_data = {}
        """
        station_data (dict):
            A dictionary containing all current weather data from the
            station specified by the station_info.
        """

    def get_station_data(self):
        """
        Method that retrieves the current weather data for the station
        specified by the saved station_info from the DWD-API.
        The recieved data is returned in form of a deserialized json file.

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
        params = {"stationIds": self.station_info.get("Stations-kennung", "0")}
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

    def get_display_data(self):
        """
        Method that extracts the weather data that will be displayed from
        the saved station_name, station_info and station_data.
        The data used for display is returned in a new DisplayData object.

        Returns
        -------
        display_data (DisplayData):
            A DisplayData object containing all weather data for the given
            station formatted for display purposes.
        """

        # Try to get the station identifier.
        stationId = self.station_info.get("Stations-kennung", "0")

        # Check whether forecast data is available.
        forecast_dict = self.station_data.get(stationId, {}).get("forecast1", {})
        if not forecast_dict:
            # Error values for time and temperature.
            date_time = None
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

            date_time = date_temp[0]
            temperature = date_temp[1]

        # Check whether days data is available.
        days_list = self.station_data.get(stationId, {}).get("days", [])
        if not days_list:
            forecast = 0
            daily_min = float("nan")
            daily_max = float("nan")
        else:
            # Find the date in days list closest to the current date.
            curr_date = datetime.datetime.now()
            day = min([da for da in days_list
                       if datetime.datetime.strptime(da["dayDate"], "%Y-%m-%d") <= curr_date],
                      key=lambda d: abs(curr_date -
                                        datetime.datetime.strptime(d["dayDate"], "%Y-%m-%d")))

            forecast = day["icon"]

            if day["temperatureMin"] < -999 or day["temperatureMin"] > 999:
                daily_min = float("nan")
            else:
                daily_min = day["temperatureMin"] / 10

            if day["temperatureMax"] < -999 or day["temperatureMax"] > 999:
                daily_max = float("nan")
            else:
                daily_max = day["temperatureMax"] / 10

        # Return all gathered data in a DisplayData object.
        return DisplayData(station_name=self.station_name, date_time=date_time,
                           temperature=temperature, forecast=forecast,
                           daily_min=daily_min, daily_max=daily_max)

    def update(self):
        """
        Method that updates or retrieves the station_data from the DWD-API with
        the informations saved in station_info.

        Returns
        -------
        success (bool):
            Indicates whether the update process was a success or not.
        """

        # Try to get station data from the DWD-API.
        station_data = self.get_station_data()

        # Check whether there is data for an update.
        if station_data:
            self.station_data = station_data
            return True
        else:
            return False
