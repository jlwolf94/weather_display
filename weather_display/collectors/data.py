"""
The data module contains the Data abstract base class that is used as
a prototype with all common methods for the specialized data classes.
"""

import math
import requests

from abc import ABC, abstractmethod


class Data(ABC):
    """
    Abstract base class that contains all common methods and method prototypes
    for the specialized data classes.
    """

    def __init__(self, station, attempts=3, timeout=10):
        """
        Constructor for the Data objects.

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

        self.attempts = attempts
        """
        attempts (int):
            Number of connection attempts.
        """

        self.url = ""
        """
        url (str):
            Standard url for the get requests.
        """

        self.params = None
        """
        params (Optional[dict[str, str]]):
            Dictionary with all parameters for the get request.
        """

        self.headers = None
        """
        headers (Optional[dict[str, str]]):
            Dictionary with all header parameters for the get request.
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
    def calc_dew_point(humidity, temperature):
        """
        Method that calculates the dew point for a given humidity and temperature.
        For the calculation an approximation formula based on the Magnus formula
        with empirically determined parameters is used. The formula is enhanced
        using the Boegel modification in form of the Arden Buck equation.
        The equation is usable between -80 degree Celsius and +50 degree Celsius.

        Parameters
        ----------
        humidity (float):
            The relative humidity of the air in percent.

        temperature (float):
            The current temperature in degree Celsius.

        Returns
        -------
        dew_point (float):
            The calculated dew point in degree Celsius for the given
            relative humidity and temperature.
        """

        # Check whether humidity and temperature are available.
        if humidity == float("nan") or temperature == float("nan"):
            return float("nan")

        # Define empirical constants for the equation.
        # k_two has no unit.
        k_two = 18.678
        # k_three is in degree Celsius.
        k_three = 257.14
        # k_four is in degree Celsius.
        k_four = 234.5

        # Calculate the result with the modified Magnus formula.
        f_one = k_two - (temperature / k_four)
        f_two = temperature / (k_three + temperature)
        gamma_m = math.log((humidity / 100) * math.exp(f_one * f_two))
        return (k_three * gamma_m) / (k_two - gamma_m)

    @abstractmethod
    def build_url(self):
        """
        Method that builds the standard url for the get requests.

        Returns
        -------
        url (str):
            Standard url for the get requests.
        """

        pass

    @abstractmethod
    def build_params(self):
        """
        Method that builds the parameters for the get requests.

        Returns
        -------
        params (dict[str, str]):
            Dictionary with all parameters for the get request.
        """

        pass

    @abstractmethod
    def build_headers(self):
        """
        Method that builds the headers for the get requests.

        Returns
        -------
        headers (dict[str, str]):
            Dictionary with all header parameters for the get request.
        """

        pass

    def get_station_response(self):
        """
        Method that triggers a get request to the standard url with the set
        parameters, headers and timeout. The method handles all possible
        error cases.

        Returns
        -------
        station_response (Optional[Response]):
            The response object of the request to the standard url with the
            set parameters and headers or None.
        """

        # Try to reach the server multiple times and handle occuring exceptions.
        for i in range(self.attempts):
            try:
                response = requests.get(url=self.url, params=self.params,
                                        headers=self.headers, timeout=self.timeout)
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

    @abstractmethod
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

        pass

    @abstractmethod
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

        pass

    def update(self):
        """
        Method that updates the station_data with data from the standard url
        using the set parameters and headers. If the specified station is
        not available then the current data is not overwritten.

        Returns
        -------
        success (bool):
            Indicates whether the update process was a success or not.
        """

        # Try to get station data from the standard url.
        station_data = self.get_station_data(self.get_station_response())

        # Check whether there is data for an update.
        if station_data:
            self.station_data = station_data
            return True
        else:
            return False
