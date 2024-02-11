"""
The data_dwd module contains the DataDWD class that is used to make all direct calls
to the DWD-API, save the received data and preprocess the received data for display
purposes.
"""

from datetime import datetime, timedelta
from functools import reduce

from weather_display.collectors.data import Data
from weather_display.models.display_data import DisplayData


class DataDWD(Data):
    """
    Class that contains the DWD-API base url and stores the station information
    used for the data requests. It stores the received data for later use or display.
    """

    def __init__(self, station, attempts=3, timeout=10):
        """
        Constructor for the DataDWD objects.

        Args:
            station (Station): Station object containing all information of the station.
            attempts (int): Number of connection attempts.
                Default value is 3.
            timeout (int): Connection timeout for a server answer in seconds.
                Default value is 10 seconds.
        """
        super().__init__(station, attempts, timeout)

        self.url = "https://app-prod-ws.warnwetter.de/v30" + "/stationOverviewExtended"
        """
        str: Standard url for the get requests.
        """

        self.params = {"stationIds": station.identifier}
        """
        dict[str, str], optional: Dictionary with all parameters for the get request.
        """

        self.headers = {"accept": "application/json"}
        """
        dict[str, str], optional: Dictionary with all header parameters for the get request.
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
        if response is not None:
            return response.json()
        else:
            return {}

    def get_display_data(self):
        """
        Method that extracts the weather data that will be displayed from
        the saved station and station_data. The data used for display is
        returned in a new DisplayData object.

        Returns:
            DisplayData: A DisplayData object containing all weather data for the set
                station formatted for display purposes.
        """
        display_data = DisplayData(station_name=self.station.name)

        forecast_dict = self.station_data.get(self.station.identifier, {}).get("forecast1", {})
        display_data = self._update_display_data_with_forecast_dict(display_data, forecast_dict)

        days_list = self.station_data.get(self.station.identifier, {}).get("days", [])
        display_data = self._update_display_data_with_days_list(display_data, days_list)

        return display_data

    def _update_display_data_with_forecast_dict(self, display_data, forecast_dict):
        if forecast_dict:
            date_start = datetime.fromtimestamp(forecast_dict["start"] / 1000)
            date_step = timedelta(milliseconds=forecast_dict["timeStep"])
            date_start_step = (date_start, date_step)

            date_temp_list = self._create_date_value_list(
                forecast_dict["temperature"], date_start_step, (-999, 999), float("nan")
            )
            date_dew_list = self._create_date_value_list(
                forecast_dict["dewPoint2m"], date_start_step, (-999, 999), float("nan")
            )
            date_pre_list = self._create_date_value_list(
                forecast_dict["precipitationTotal"], date_start_step, (0, 999), 0.0
            )

            return self._update_display_data_with_value_lists(
                display_data, date_temp_list, date_dew_list, date_pre_list
            )
        else:
            return display_data

    def _update_display_data_with_days_list(self, display_data, days_list):
        if days_list:
            day = self._get_day_closest_to_current_date(days_list)
            return self._update_display_data_with_day(display_data, day)
        else:
            return display_data

    def _update_display_data_with_value_lists(
        self, display_data, date_temp_list, date_dew_list, date_pre_list
    ):
        date_temp = self._get_date_temp_closest_to_current_date(date_temp_list)
        display_data.date_time = date_temp[0]
        display_data.temperature = date_temp[1]

        # Use the found date_time to find the dew point.
        display_data.dew_point = next(
            (dd[1] for dd in date_dew_list if dd[0] == date_temp[0]), float("nan")
        )

        # Add up all precipitation data per hour to get the precipitation per day.
        display_data.precipitation = reduce(
            lambda x, y: x + y, [dp[1] for dp in date_pre_list if dp[0] <= date_temp[0]], 0.0
        )

        return display_data

    @staticmethod
    def _create_date_value_list(forecast_dict_value, date_start_step, limits, default_value):
        date_start, date_step = date_start_step
        lower_limit, upper_limit = limits
        date_value_list = []
        for step, value in enumerate(forecast_dict_value):
            if value < lower_limit or value > upper_limit:
                date_value_list.append((date_start + (step * date_step), default_value))
            else:
                date_value_list.append((date_start + (step * date_step), value / 10))
        return date_value_list

    @staticmethod
    def _get_date_temp_closest_to_current_date(date_temp_list):
        curr_date = datetime.now()
        date_temp = min(
            [dt for dt in date_temp_list if dt[0] <= curr_date], key=lambda t: abs(curr_date - t[0])
        )
        return date_temp

    @staticmethod
    def _get_day_closest_to_current_date(days_list):
        curr_date = datetime.now()
        day = min(
            [da for da in days_list if datetime.strptime(da["dayDate"], "%Y-%m-%d") <= curr_date],
            key=lambda d: abs(curr_date - datetime.strptime(d["dayDate"], "%Y-%m-%d")),
        )
        return day

    @staticmethod
    def _update_display_data_with_day(display_data, day):
        display_data.forecast = day["icon"]
        if -999 <= day["temperatureMin"] <= 999:
            display_data.daily_min = day["temperatureMin"] / 10
        if -999 <= day["temperatureMax"] <= 999:
            display_data.daily_max = day["temperatureMax"] / 10
        return display_data
