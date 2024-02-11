"""
The data_w24 module contains the DataW24 class that is used to download and parse
the wetter24 website, save the data and preprocess the extracted data for display purposes.
"""

import json
from datetime import datetime

from bs4 import BeautifulSoup

from weather_display.collectors.data import Data
from weather_display.models.display_data import DisplayData


class DataW24(Data):
    """
    Class that contains the wetter24 base url and stores the station information
    used for the website requests. It stores the received data for later use or display.
    """

    def __init__(self, station, attempts=3, timeout=10):
        """
        Constructor for the DataW24 objects.

        Args:
            station (Station): Station object containing all information of the station.
            attempts (int): Number of connection attempts.
                Default value is 3.
            timeout (int): Connection timeout for a server answer in seconds.
                Default value is 10 seconds.
        """
        super().__init__(station, attempts, timeout)

        self.url = (
            "http://www.wetter24.de/wetterstation"
            + "/"
            + station.name.lower()
            + "/"
            + str(station.number)
        )
        """
        str: Standard url for the get requests.
        """

        self.params = None
        """
        dict[str, str], optional: Dictionary with all parameters for the get request.
        """

        user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) " + "Gecko/20100101 Firefox/114.0"
        )

        self.headers = {"User-Agent": user_agent}
        """
        dict[str, str]: Dictionary with all header parameters for the get request.
        """

    def get_station_data(self, response):
        """
        Method that processes the response of a request to the standard url
        with set parameters and headers. It returns a formatted dictionary of the data.

        Args:
            response (Response, optional): A response object retrieved from a request
                to the standard url with the set parameters and headers or None.

        Returns:
            dict: A dictionary containing all current weather data from the
                station specified by station.
        """
        if response is None:
            return {}

        page = BeautifulSoup(response.content, features="lxml")

        # Extract all script tags of main.
        scripts = page.find("main").find_all("script", recursive=False)

        # If there are no two script tags, then an error occurred.
        if len(scripts) != 2:
            return {}

        # The script tag content contains all weather data of the station.
        data_string = scripts[0].get_text().split("initWeatherStation(")[1].split(")")[0]
        return json.loads(data_string)

    def get_display_data(self):
        """
        Method that extracts the weather data that will be displayed from the saved
        station and station_data. The data used for display is returned in
        a new DisplayData object.

        Returns:
            DisplayData: A DisplayData object containing all weather data for the set
                station formatted for display purposes.
        """
        display_data = DisplayData(station_name=self.station.name)

        temp_dict = self.station_data.get("temperatures", {})
        display_data = self._update_display_data_with_temp_dict(display_data, temp_dict)

        prec_dict = self.station_data.get("precipitation", {})
        display_data = self._update_display_data_with_prec_dict(display_data, prec_dict)

        return display_data

    def _update_display_data_with_temp_dict(self, display_data, temp_dict):
        if temp_dict:
            temp_list = temp_dict.get("measuredTemperature", [])
            display_data = self._update_display_data_date_time_and_temp(display_data, temp_list)
            display_data = self._update_display_data_daily_min_and_max(display_data, temp_list)

            dew_point_list = temp_dict.get("dewpoints", [])
            display_data = self._update_display_data_dew_point(display_data, dew_point_list)

            return display_data
        else:
            return display_data

    @staticmethod
    def _update_display_data_with_prec_dict(display_data, prec_dict):
        if prec_dict:
            prec_list = prec_dict.get("daily", [])
            if prec_list:
                display_data.precipitation = 0.0 if prec_list[-1] is None else float(prec_list[-1])
            else:
                display_data.precipitation = 0.0
            return display_data
        else:
            return display_data

    @staticmethod
    def _update_display_data_date_time_and_temp(display_data, temp_list):
        for temp in reversed(temp_list):
            if temp[1] is not None:
                display_data.date_time = datetime.fromtimestamp(temp[0] / 1000)
                display_data.temperature = float(temp[1])
                break
        return display_data

    def _update_display_data_daily_min_and_max(self, display_data, temp_list):
        if display_data.date_time is not None:
            curr_date = display_data.date_time.replace(hour=0, minute=0)
            daily_min, daily_max = self._get_daily_min_and_max(curr_date, temp_list)
            if daily_min != float("inf"):
                display_data.daily_min = daily_min
            if daily_max != float("-inf"):
                display_data.daily_max = daily_max
            return display_data
        else:
            return display_data

    @staticmethod
    def _get_daily_min_and_max(curr_date, temp_list):
        daily_min = float("inf")
        daily_max = float("-inf")
        for temp in reversed(temp_list):
            if temp[1] is not None:
                if datetime.fromtimestamp(temp[0] / 1000) < curr_date:
                    break
                else:
                    curr_temp = float(temp[1])
                    if curr_temp < daily_min:
                        daily_min = curr_temp
                    if curr_temp > daily_max:
                        daily_max = curr_temp
        return daily_min, daily_max

    @staticmethod
    def _update_display_data_dew_point(display_data, dew_point_list):
        for dew_point in reversed(dew_point_list):
            if dew_point[1] is not None:
                display_data.dew_point = float(dew_point[1])
                break
        return display_data
