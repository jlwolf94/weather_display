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
    Class that contains the wetter24 base url and stores the station informations
    used for the website requests. It stores the received data for later use or display.
    """

    def __init__(self, station, attempts=3, timeout=10):
        """
        Constructor for the DataW24 objects.

        Parameters
        ----------
        station (Station):
            Station object containing all informations of the station.

        attempts (int):
            Number of connection attempts. Default value is 3.

        timeout (int):
            Connection timeout for a server answer in seconds.
            Default value is 10 seconds.
        """

        super().__init__(station, attempts, timeout)

        self.url = "http://www.wetter24.de/wetterstation" + "/" \
            + station.name.lower() + "/" + str(station.number)
        """
        url (str):
            Standard url for the get requests.
        """

        self.params = None
        """
        params (Optional[dict[str, str]]):
            Dictionary with all parameters for the get request.
        """

        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) " \
            + "Gecko/20100101 Firefox/114.0"
        self.headers = {"User-Agent": user_agent}
        """
        headers (Optional[dict[str, str]]):
            Dictionary with all header parameters for the get request.
        """

    def get_station_data(self, response):
        """
        Method that processes the response of a request to the
        standard url with set parameters and headers. It returns
        a formatted dictionary of the data.

        Parameters
        ----------
        response (Optional[Response]):
            A response object retrieved from a request to the standard url
            with the set parameters and headers or None.

        Returns
        -------
        station_data (dict):
            A dictionary containing all current weather data from the
            station specified by station.
        """

        # Check whether response data is available.
        if response is None:
            return {}

        # Convert the response content to a searchable object.
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
        Method that extracts the weather data that will be displayed from
        the saved station and station_data. The data used for display is
        returned in a new DisplayData object.

        Returns
        -------
        display_data (DisplayData):
            A DisplayData object containing all weather data for the set
            station formatted for display purposes.
        """

        # Create the result DisplayData object.
        display_data = DisplayData(station_name=self.station.name)

        # Check whether temperature data is available.
        temp_dict = self.station_data.get("temperatures", {})
        if temp_dict:
            # Extract the current temperature with its date.
            temp_list = temp_dict.get("measuredTemperature", [])
            for temp in reversed(temp_list):
                if temp[1] is not None:
                    display_data.date_time = datetime.fromtimestamp(temp[0] / 1000)
                    display_data.temperature = float(temp[1])
                    break

            # Search for min and max temperature of the day.
            if display_data.date_time is not None:
                curr_date = display_data.date_time.replace(hour=0, minute=0)
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

                if daily_min != float("inf"):
                    display_data.daily_min = daily_min
                if daily_max != float("-inf"):
                    display_data.daily_max = daily_max

            # Extract current dew point.
            dew_point_list = temp_dict.get("dewpoints", [])
            for dew_point in reversed(dew_point_list):
                if dew_point[1] is not None:
                    display_data.dew_point = float(dew_point[1])
                    break

        # Check whether precipitation data is available.
        prec_dict = self.station_data.get("precipitation", {})
        if prec_dict:
            # Extract the current precipitation per day.
            prec_list = prec_dict.get("daily", [])
            if prec_list:
                display_data.precipitation = (0.0 if prec_list[-1] is None
                                              else float(prec_list[-1]))
            else:
                display_data.precipitation = 0.0

        # Return all gathered data in a DisplayData object.
        return display_data
