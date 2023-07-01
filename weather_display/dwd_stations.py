"""
The dwd_stations module contains the DwdStations class that is used to retrieve
all stations listed on the corresponding DWD website and to convert this list
to a processable json file. The class handles all needed request and I/O processes.
"""

import datetime
import json
import requests

from bs4 import BeautifulSoup
from pathlib import Path


class DwdStations:

    def __init__(self, url=None, params=None, headers=None, timeout=15, file_name=None):
        if url is not None:
            self.url = url
        else:
            self.url = "https://www.dwd.de/DE/leistungen/klimadatendeutschland/" \
                + "statliste/statlex_html.html"

        if params is not None:
            self.params = params
        else:
            self.params = {"view": "nasPublication", "nn": "16102"}

        if headers is not None:
            self.headers = headers
        else:
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) " \
                + "Gecko/20100101 Firefox/114.0"
            self.headers = {"User-Agent": user_agent}

        self.timeout = timeout

        if file_name is not None:
            self.file_name = str(file_name) + ".json"
        else:
            self.file_name = "dwd_stations.json"

        self.table_entries = []

    @staticmethod
    def process_stations_page(response):
        stations_page = BeautifulSoup(response.content, features="lxml")

        # Extract the table from the page and convert it to a json file.
        table = stations_page.find("table")
        column_names = []
        table_entries = []

        # Find all column names.
        for tr in table.find_all("tr", recursive=False):
            for th in tr.find_all("th", recursive=False):
                if th.text != "Stationslexikon":
                    column_names.append(th.text)

        # Find all column entries and add them to the list of entries.
        for tr in table.find_all("tr", recursive=False):
            entry = {}
            for i, td in enumerate(tr.find_all("td", recursive=False)):
                entry[column_names[i]] = str(td.text).replace(u"\xa0", u" ")
            if entry:
                table_entries.append(entry)

        return table_entries

    def get_stations_page(self):
        # Try three times to reach the server.
        for i in range(3):
            try:
                response = requests.get(self.url, params=self.params,
                                        headers=self.params, timeout=self.timeout)
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
        # Get the table entries by processing the server response.
        response = self.get_stations_page()
        if response is not None:
            return self.process_stations_page(response)
        else:
            return []

    def save_table_as_json(self, table_entries):
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

    def update(self):
        # Get the path to the json file.
        file_path = Path(__file__).parents[1].joinpath("data", self.file_name)

        # Check whether the file already exists.
        if file_path.is_file():
            mod_date = \
                datetime.datetime.fromtimestamp(file_path.stat().st_mtime).strftime("%d.%m.%Y")
            curr_date = datetime.datetime.now().strftime("%d.%m.%Y")

            # Check whether the file is already updated and get the stations from the file.
            if mod_date == curr_date:
                try:
                    with file_path.open(encoding="utf-8") as file:
                        self.table_entries = json.load(file)
                        return True
                except OSError as err_os:
                    print("I/O Error:", err_os)
                    return False

        # Update the table entries and the json file.
        table_entries = self.get_table_entries()
        self.table_entries = table_entries
        return self.save_table_as_json(table_entries)
