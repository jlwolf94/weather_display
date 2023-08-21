"""
The w24_data module contains the W24Data class that is used to download and parse
the wetter24 website, save the data and preprocess the extracted data for display purposes.
"""

import json
import requests

from datetime import datetime
from bs4 import BeautifulSoup
from weather_display.models.display_data import DisplayData


class W24Data:
    """
    Class that contains the wetter24 base url and stores the station informations
    used for the website requests. It stores the received data for later use or display.
    """

    def __init__(self, station, attempts=3, timeout=10):
        """
        Constructor for the W24Data objects.

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

        self.station = station
        """
        station (Station):
            Station object containing all informations of the station.
        """

        self.url = "http://www.wetter24.de/wetterstation"
        """
        url (str):
            Standard base url for the wetter24 weather station site.
        """

        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) " \
            + "Gecko/20100101 Firefox/114.0"
        self.headers = {"User-Agent": user_agent}
        """
        headers (dict[str, str]):
            Dictionary with all header parameters for the request.
        """

        self.attempts = attempts
        """
        attempts (int):
            Number of connection attempts.
        """

        self.timeout = timeout
        """
        timeout (int):
            Connection timeout for a server answer in seconds.
        """

        self.station_data = {}
        """
        station_data (dict):
            A dictionary containing all current weather data from the
            station specified by station.
        """

    @staticmethod
    def process_stations_page(response):
        """
        Method that processes the response of a request to the
        standard url and returns a formatted dictionary of the data.

        Parameters
        ----------
        response (Optional[Response]):
            A response object retrieved from a request to the standard url
            or None.

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

        # Extract the first script tag of main.
        script = page.find("main").find("script", recursive=False)

        # The script tag content contains all weather data of the station.
        data_string = script.get_text().split("initWeatherStation(")[1].split(")")[0]
        return json.loads(data_string)

    def get_station_data(self):
        """
        Method that triggers a get request for the standard url and
        handles all possible error cases.

        Returns
        -------
        response (Optional[Response]):
            The response object of the request to the standard url or None.
        """

        # Add station name and number to the base url for the get request.
        url = self.url + "/" + self.station.name.lower() + "/" + str(self.station.number)

        # Try to reach the server multiple times and handle occuring exceptions.
        for i in range(self.attempts):
            try:
                response = requests.get(url, headers=self.headers,
                                        timeout=self.timeout)
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
                return response

        return None

    def get_display_data(self):
        """
        Method that extracts the weather data that will be displayed from
        the saved station and station_data. The data used for display is
        returned in a new DisplayData object.

        Returns
        -------
        display_data (DisplayData):
            A DisplayData object containing all weather data for the given
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
            # Extract the current precipitation.
            prec_list = prec_dict.get("hourly", [])
            for prec in reversed(prec_list):
                if prec[1] is not None:
                    display_data.precipitation = float(prec[1])
                    break

        # Return all gathered data in a DisplayData object.
        return display_data

    def update(self):
        """
        Method that updates or retrieves the station_data from the wetter24 website
        with the informations saved in station.

        Returns
        -------
        success (bool):
            Indicates whether the update process was a success or not.
        """

        # Try to get station data from the wetter24 website.
        station_data = self.process_stations_page(self.get_station_data())

        # Check whether there is data for an update.
        if station_data:
            self.station_data = station_data
            return True
        else:
            return False
