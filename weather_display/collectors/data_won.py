"""
The data_won module contains the DataWon class that is used to download and parse
the wetteronline website, save the data and preprocess the extracted data for
display purposes.
"""

from datetime import datetime, date
from functools import reduce

from bs4 import BeautifulSoup

from weather_display.collectors.data import Data
from weather_display.models.display_data import DisplayData


class DataWon(Data):
    """
    Class that contains the wetteronline base url and stores the station information
    used for the website requests. It stores the received data for later use or display.
    """

    DATE_TIME_FORMAT_STRING = "%d.%m.%Y %H:%M"
    """
    str: Format used to convert date time strings to datetime objects.
    """

    NO_VALUE_MESSAGE = "keine Meldung"
    """
    str: Message string when no value is present.
    """

    def __init__(self, station, attempts=3, timeout=10):
        """
        Constructor for the DataWon objects.

        Args:
            station (Station): Station object containing all information of the station.
            attempts (int): Number of connection attempts.
                Default value is 3.
            timeout (int): Connection timeout for a server answer in seconds.
                Default value is 10 seconds.
        """
        super().__init__(station, attempts, timeout)

        self.url = "https://www.wetteronline.de/wetter-aktuell" + "/" + station.name.lower()
        """
        str: Standard url for the get requests.
        """

        self.params = {"iid": station.identifier}
        """
        dict[str, str]: Dictionary with all parameters for the get request.
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

        # Extract the div with all tables and check whether it exists.
        table_div = page.find("div", id="showcase")
        if table_div is None:
            return {}

        tables = self._extract_tables(table_div)
        row_data_list = self._extract_row_data_list(tables)
        temperature_data = self._extract_temperature_data(row_data_list)
        humidity_data = self._extract_humidity_data(row_data_list)
        precipitation_data = self._extract_precipitation_data(row_data_list)

        return {
            "temperatures": temperature_data,
            "humidities": humidity_data,
            "precipitations": precipitation_data,
        }

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

        # Check whether temperature data is available.
        temp_list = self.station_data.get("temperatures", [])
        if temp_list:
            # Extract the current temperature with its date and time.
            display_data.date_time = temp_list[0][0]
            display_data.temperature = temp_list[0][1]

            # Search for min and max temperature of the day.
            if display_data.date_time is not None:
                curr_date = display_data.date_time.replace(hour=0, minute=0)
                daily_min = float("inf")
                daily_max = float("-inf")
                for temp in temp_list:
                    if temp[0] < curr_date:
                        break
                    else:
                        curr_temp = temp[1]
                        if curr_temp < daily_min:
                            daily_min = curr_temp
                        if curr_temp > daily_max:
                            daily_max = curr_temp

                if daily_min != float("inf"):
                    display_data.daily_min = daily_min
                if daily_max != float("-inf"):
                    display_data.daily_max = daily_max

        # Check whether humidity data is available.
        humi_list = self.station_data.get("humidities", [])
        if humi_list:
            # Calculate the current dew point.
            display_data.dew_point = self.calc_dew_point(
                humidity=humi_list[0][1], temperature=display_data.temperature
            )

        # Check whether precipitation data is available.
        prec_list = self.station_data.get("precipitations", [])
        if prec_list:
            # Extract the precipitation per day.
            display_data.precipitation = reduce(
                lambda x, y: x + y, [prec[1] for prec in prec_list if prec[0].minute == 0], 0.0
            )

        return display_data

    @staticmethod
    def _extract_tables(table_div):
        return [
            table_div.find("div", id="temperature", recursive=False),
            table_div.find("div", id="humidity", recursive=False),
            table_div.find("div", id="precipitation", recursive=False),
        ]

    @staticmethod
    def _extract_row_data_list(tables):
        rows_list = [
            (
                table.find("table", attrs={"class": "hourly"}, recursive=False)
                .find("tbody", recursive=False)
                .find_all("tr", recursive=False)
            )
            for table in tables
        ]
        return [
            [[td.get_text() for td in row.find_all("td", recursive=False)] for row in rows]
            for rows in rows_list
        ]

    def _extract_temperature_data(self, row_data_list):
        return [
            [self._convert_date_time_string(data[0]), self._convert_temperature_string(data[1])]
            for data in row_data_list[0]
        ]

    def _extract_humidity_data(self, row_data_list):
        return [
            [self._convert_date_time_string(data[0]), self._convert_humidity_string(data[1])]
            for data in row_data_list[1]
        ]

    def _extract_precipitation_data(self, row_data_list):
        return [
            [self._convert_date_time_string(data[0]), self._convert_precipitation_string(data[1])]
            for data in row_data_list[2]
        ]

    @staticmethod
    def _convert_date_time_string(date_time):
        if date_time == "" or date_time == "-" or date_time == DataWon.NO_VALUE_MESSAGE:
            return datetime.strptime("01.01.1970 00:00", DataWon.DATE_TIME_FORMAT_STRING)
        else:
            dt_list = date_time.split(" ")
            return datetime.strptime(
                dt_list[1] + str(date.today().year) + " " + dt_list[2],
                DataWon.DATE_TIME_FORMAT_STRING,
            )

    @staticmethod
    def _convert_temperature_string(temperature):
        # Split the unit from the number.
        number_string = temperature.split("°")[0]
        if number_string == "" or number_string == "-" or number_string == DataWon.NO_VALUE_MESSAGE:
            return float("nan")
        else:
            return float(number_string)

    @staticmethod
    def _convert_humidity_string(humidity):
        # Split the unit from the number.
        number_string = humidity.split("%")[0]
        if number_string == "" or number_string == "-" or number_string == DataWon.NO_VALUE_MESSAGE:
            return float("nan")
        else:
            return float(number_string)

    @staticmethod
    def _convert_precipitation_string(precipitation):
        if precipitation == "" or precipitation == "-" or precipitation == DataWon.NO_VALUE_MESSAGE:
            return 0.0
        else:
            # Split the unit and check whether there is a sign for the number.
            number_string = precipitation.split(" ")[0]
            if number_string[0].isdigit():
                return float(number_string)
            else:
                return float(number_string[1:])
