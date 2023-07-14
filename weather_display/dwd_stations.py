"""
The dwd_stations module contains the DwdStations class that is used to retrieve
all stations listed on the corresponding DWD website and to convert the table
to a processable json file. The class handles all needed request and I/O processes.
"""

import datetime
import json
import math
import requests

from pathlib import Path
from bs4 import BeautifulSoup


class DwdStations:
    """
    Class that contains all methods and data necessary to retrieve the latest
    DWD stations table. The stations table is saved to a json file and is
    updated after the set amount of time.
    """

    def __init__(self, attempts=3, timeout=10, refresh=24, file_name="dwd_stations.json"):
        """
        Constructor for the DwdStations objects.

        Parameters
        ----------
        attempts (int):
            Number of connection attempts. Default value is 3.

        timeout (int):
            Connection timeout for a server answer in seconds.
            Default value is 10 seconds.

        refresh (int):
            Refresh time in hours for the saved json file.
            Default value is 24 hours.

        file_name (str):
            File name for the json file with all station data.
            Default name is dwd_stations.json.
        """

        self.url = "https://www.dwd.de/DE/leistungen/klimadatendeutschland/" \
            + "statliste/statlex_html.html"
        """
        url (str):
            Standard url pointing to the location of the table with all stations
            and their corresponding informations.
        """

        self.params = {"view": "nasPublication", "nn": "16102"}
        """
        params (dict):
            Dictionary with all url parameters for the request.
        """

        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) " \
            + "Gecko/20100101 Firefox/114.0"
        self.headers = {"User-Agent": user_agent}
        """
        headers (dict):
            Dictionary with all header parameters for the request.
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

        self.refresh = refresh
        """
        refresh (int):
            Refresh time in hours for the saved json file.
            Default value is 24 hours.
        """

        self.file_name = file_name
        """
        file_name (str):
            File name for the json file with all station data.
            Default name is dwd_stations.json.
        """

        self.table_entries = {}
        """
        table_entries (dict):
            A dictionary containing all stations from the stations table.
            The dictionary uses the station names as keys and the
            corresponding values are dictionaries filled with the
            additional station informations.
        """

    @staticmethod
    def process_stations_page(response):
        """
        Method that processes the response content of a request to the
        standard url and returns a formatted dictionary of the stations
        with their informations.

        Parameters
        ----------
        response (Response):
            A response object retrieved from a request to the standard url.

        Returns
        -------
        table_entries (dict):
            A dictionary containing all stations from the stations table.
            The dictionary uses the station names as keys and the
            corresponding values are dictionaries filled with the
            additional station informations.
        """

        # Convert the response content to a searchable object.
        stations_page = BeautifulSoup(response.content, features="lxml")

        # Extract the table rows from the table in the stations page.
        table_rows = stations_page.find("table").find_all("tr", recursive=False)

        # Get all column names in a list.
        column_names = [th.get_text()
                        for th in table_rows[1].find_all("th", recursive=False)]

        # Find all column entries and add them with their column name
        # to the dictionary with all table entries.
        table_entries = {}
        for tr in table_rows[2:]:

            station_name = ""
            station_info = {}
            for i, td in enumerate(tr.find_all("td", recursive=False)):
                if i == 0:
                    station_name = td.get_text().replace("\xa0", " ")
                else:
                    station_info.update(
                        {column_names[i]: td.get_text().replace("\xa0", " ")})

            if station_info.get("Kennung", "") == "SY":
                table_entries.update({station_name: station_info})

        return table_entries

    def get_stations_page(self):
        """
        Method that triggers a get request for the standard url and
        handles all possible error cases.

        Returns
        -------
        response (Optional[Response]):
            The response object of the request to the standard url or None.
        """

        # Try to reach the server multiple times and handle occuring exceptions.
        for i in range(self.attempts):
            try:
                response = requests.get(self.url, params=self.params,
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

    def get_table_entries(self):
        """
        Method that triggers a request to the standard url and processes the
        data in the response by using the already defined methods.

        Returns
        -------
        table_entries (dict):
            A dictionary containing all stations from the stations table.
            The dictionary uses the station names as keys and the
            corresponding values are dictionaries filled with the
            additional station informations. With no data an empty
            dictionary is returned.
        """

        # Get the table entries by processing the server response.
        response = self.get_stations_page()
        if response is not None:
            return self.process_stations_page(response)
        else:
            return {}

    def get_station_info_by_name(self, station_name):
        """
        Method that searches a station identified by its name in the
        saved stations table and returns the informations of the station
        if it is found.

        Parameters
        ----------
        station_name (str):
            The name of the searched station.

        Returns
        -------
        station_info (dict):
            A dictionary containing the station name together with the
            informations of the station or an empty dictionary
            if the station is not found.
        """

        # Try to get the informations for the searched station.
        info = self.table_entries.get(station_name, {})
        return {station_name: info} if info else {}

    def get_station_info_by_distance(self, latitude, longitude):
        """
        Method that searches the station closest to the current position which
        is represented by the latitude and longitude value. The informations
        of the closest station with hourly measurements are returned.

        Parameters
        ----------
        latitude (float):
            The current geographic latitude.

        longitude (float):
            The current geographic longitude.

        Returns
        -------
        station_info (dict):
            A dictionary containing the station name together with the
            informations of the station or an empty dictionary
            if the station is not found.
        """

        # Check whether data for a search is available.
        if self.table_entries:
            # Search for the closest station.
            min_distance = float("inf")
            min_station = {}
            for stn, sti in self.table_entries.items():
                curr_distance = \
                    math.dist((latitude, longitude),
                              (float(sti["Breite"]), float(sti["Länge"])))

                if curr_distance < min_distance:
                    min_distance = curr_distance
                    min_station = {stn: sti}

            return min_station
        else:
            return {}

    def save_table_as_json(self, table_entries):
        """
        Method that saves the given table entries to a json file
        with the set file name. The file is placed in the data directory.

        Parameters
        ----------
        table_entries (dict):
            A dictionary containing all stations from the stations table.
            The dictionary uses the station names as keys and the
            corresponding values are dictionaries filled with the
            additional station informations.

        Returns
        -------
        success (bool):
            Indicates whether the save process was a success or not.
        """

        # Get the path to the json file.
        file_path = Path(__file__).parents[1].joinpath("data", self.file_name)

        # Create parent directory if necessary.
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Check whether data is available.
        if not table_entries:
            print("Data Error: No data available to write to json file.")
            return False

        # Write all table entries to the json file.
        try:
            with file_path.open(mode="w", encoding="utf-8") as file:
                json.dump(table_entries, file, ensure_ascii=False, indent=4)
        except OSError as err_os:
            print("I/O Error:", err_os)
            return False

        return True

    def load_table_from_json(self):
        """
        Method that loads the table entries from a json file with the
        set file name. The file needs to be in the data directory.

        Returns
        -------
        table_entries (dict):
            A dictionary containing all stations from the stations table.
            The dictionary uses the station names as keys and the
            corresponding values are dictionaries filled with the
            additional station informations.
        """

        # Get the path to the json file.
        file_path = Path(__file__).parents[1].joinpath("data", self.file_name)

        # Try to load the data if the file exists.
        if file_path.is_file():
            try:
                with file_path.open(encoding="utf-8") as file:
                    return json.load(file)
            except OSError as err_os:
                print("I/O Error:", err_os)
                return {}
        else:
            print("I/O Error: File does not exist.")
            return {}

    def update(self):
        """
        Method that updates or retrieves the stations table by checking the
        current data and calling all neccessary methods for the update.

        Returns
        -------
        success (bool):
            Indicates whether the update process was a success or not.
        """

        # Get the path to the json file.
        file_path = Path(__file__).parents[1].joinpath("data", self.file_name)

        # Check whether the file already exists.
        if file_path.is_file():
            mod_date = datetime.datetime.fromtimestamp(file_path.stat().st_mtime)
            curr_date = datetime.datetime.now()

            # Check whether the file is already updated and get the stations from the file.
            if curr_date - mod_date <= datetime.timedelta(hours=self.refresh):
                table_entries = self.load_table_from_json()

                # Check whether data is available.
                if table_entries:
                    self.table_entries = table_entries
                    return True
                else:
                    print("Data Error: No data available from json file.")
                    return False
            else:
                # Update the table entries and the json file.
                table_entries = self.get_table_entries()
                self.table_entries = table_entries

                if self.save_table_as_json(table_entries):
                    # Update was successful.
                    return True
                else:
                    # Fall back to existing file if saving failed.
                    table_entries = self.load_table_from_json()

                    # Check whether data is available.
                    if table_entries:
                        self.table_entries = table_entries
                        return True
                    else:
                        print("Data Error: No data available from json file.")
                        return False
        else:
            # Update the table entries and the json file.
            table_entries = self.get_table_entries()
            self.table_entries = table_entries
            return self.save_table_as_json(table_entries)
