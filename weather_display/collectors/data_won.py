"""
The data_won module contains the DataWon class that is used to download and parse
the wetteronline website, save the data and preprocess the extracted data for
display purposes.
"""

from datetime import datetime, date
from bs4 import BeautifulSoup
from weather_display.collectors.data import Data
from weather_display.models.display_data import DisplayData


class DataWon(Data):
    """
    Class that contains the wetteronline base url and stores the station informations
    used for the website requests. It stores the received data for later use or display.
    """

    def __init__(self, station, attempts=3, timeout=10):
        """
        Constructor for the DataWon objects.

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

        self.url = "https://www.wetteronline.de/wetter-aktuell" \
            + "/" + station.name.lower()
        """
        url (str):
            Standard url for the get requests.
        """

        self.params = {"iid": station.identifier}
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

    def convert_datetime_string(self, date_time):
        """
        Method that converts a given date and time from its string representation
        to a datetime object.

        Parameters
        ----------
        date_time (str):
            A string that contains a date and a time.

        Returns
        -------
        date_time (datetime):
            A new datetime object with the given date and time or
            the epoch as datetime object.
        """

        # Format for the date time string.
        format_string = "%d.%m.%Y %H:%M"

        if (date_time == "" or date_time == "-"
            or date_time == "keine Meldung"):
            return datetime.strptime("01.01.1970 00:00", format_string)
        else:
            dt_list = date_time.split(" ")
            return datetime.strptime(
                dt_list[1] + str(date.today().year) + " " + dt_list[2],
                format_string)

    def convert_temperature_string(self, temperature):
        """
        Method that converts a given temperature string to its float representation.

        Parameters
        ----------
        temperature (str):
            A string that contains the temperature with its unit.

        Returns
        -------
        temperature (float):
            A float number representing the given temperature.
        """

        # Split the unit from the number.
        number_string = temperature.split("°")[0]

        if (number_string == "" or number_string == "-"
            or number_string == "keine Meldung"):
            return float("nan")
        else:
            return float(number_string)

    def convert_humidity_string(self, humidity):
        """
        Method that converts a given humidity string to its float representation.

        Parameters
        ----------
        humidity (str):
            A string that contains the humidity with its unit.

        Returns
        -------
        humidity (float):
            A float number representing the given humidity.
        """

        # Split the unit from the number.
        number_string = humidity.split("%")[0]

        if (number_string == "" or number_string == "-"
            or number_string == "keine Meldung"):
            return float("nan")
        else:
            return float(number_string)

    def convert_precipitation_string(self, precipitation):
        """
        Method that converts a given precipitation string to its float representation.

        Parameters
        ----------
        precipitation (str):
            A string that contains the precipitation with its unit.

        Returns
        -------
        precipitation (float):
            A float number representing the given precipitation.
        """

        if (precipitation == "" or precipitation == "-"
            or precipitation == "keine Meldung"):
            return float("nan")
        else:
            # Split the unit and check whether there is a sign for the number.
            number_string = precipitation.split(" ")[0]
            if number_string[0].isdigit():
                return float(number_string)
            else:
                return float(number_string[1:])

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

        # Extract the div with all tables and check whether it exists.
        table_div = page.find("div", id="showcase")
        if table_div is None:
            return {}

        # Extract the three tables.
        tables = [table_div.find("div", id="temperature", recursive=False),
                  table_div.find("div", id="humidity", recursive=False),
                  table_div.find("div", id="precipitation", recursive=False)]

        # Extract the rows of each table and the data of each row.
        rows_list = [(table.find("table", attrs={"class": "hourly"}, recursive=False)
                      .find("tbody", recursive=False)
                      .find_all("tr", recursive=False))
                     for table in tables]
        row_data_list = [[[td.get_text() for td in row.find_all("td", recursive=False)]
                          for row in rows] for rows in rows_list]

        # Convert data for each of the three tables.
        temperature_data = [[self.convert_datetime_string(data[0]),
                             self.convert_temperature_string(data[1])]
                            for data in row_data_list[0]]
        humidity_data = [[self.convert_datetime_string(data[0]),
                          self.convert_humidity_string(data[1])]
                         for data in row_data_list[1]]
        precipitation_data = [[self.convert_datetime_string(data[0]),
                               self.convert_precipitation_string(data[1])]
                              for data in row_data_list[2]]

        # Return the extracted data in a dictionary.
        return {"temperatures": temperature_data,
                "humidities": humidity_data,
                "precipitations": precipitation_data}

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
            display_data.dew_point = \
                self.calc_dew_point(humidity=humi_list[0][1],
                                    temperature=display_data.temperature)

        # Check whether precipitation data is available.
        prec_list = self.station_data.get("precipitations", [])
        if prec_list:
            # Extract the current precipitation.
            display_data.precipitation = prec_list[0][1]

        # Return all gathered data in a DisplayData object.
        return display_data
