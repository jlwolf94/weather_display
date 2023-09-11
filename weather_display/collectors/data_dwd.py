"""
The data_dwd module contains the DataDWD class that is used to make all direct calls
to the DWD-API, save the received data and preprocess the received data for display
purposes.
"""

from datetime import datetime, timedelta
from weather_display.collectors.data import Data
from weather_display.models.display_data import DisplayData


class DataDWD(Data):
    """
    Class that contains the DWD-API base url and stores the station informations
    used for the data requests. It stores the received data for later use or display.
    """

    def __init__(self, station, attempts=3, timeout=10):
        """
        Constructor for the DwdData objects.

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

        self.url = "https://app-prod-ws.warnwetter.de/v30" + "/stationOverviewExtended"
        """
        url (str):
            Standard url for the get requests.
        """

        self.params = {"stationIds": station.identifier}
        """
        params (Optional[dict[str, str]]):
            Dictionary with all parameters for the get request.
        """

        self.headers = {"accept": "application/json"}
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

        if response is not None:
            return response.json()
        else:
            return {}

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

        # Check whether forecast data is available.
        forecast_dict = self.station_data.get(self.station.identifier, {}).get("forecast1", {})
        if forecast_dict:
            # Extract start date and date step.
            start_date = datetime.fromtimestamp(forecast_dict["start"] / 1000)
            date_step = timedelta(milliseconds=forecast_dict["timeStep"])

            # Process the temperature list by adding the time to each temperature.
            date_temp_list = []
            for step, temp in enumerate(forecast_dict["temperature"]):
                if temp < -999 or temp > 999:
                    date_temp_list.append((start_date + (step * date_step), float("nan")))
                else:
                    date_temp_list.append((start_date + (step * date_step), temp / 10))

            # Process the dew point list by adding the time to each dew_point.
            date_dew_list = []
            for step, dew in enumerate(forecast_dict["dewPoint2m"]):
                if dew < -999 or dew > 999:
                    date_dew_list.append((start_date + (step * date_step), float("nan")))
                else:
                    date_dew_list.append((start_date + (step * date_step), dew / 10))

            # Process the precipitation list by adding the time to each precipitation.
            date_pre_list = []
            for step, pre in enumerate(forecast_dict["precipitationTotal"]):
                if pre < 0 or pre > 999:
                    date_pre_list.append((start_date + (step * date_step), float("nan")))
                else:
                    date_pre_list.append((start_date + (step * date_step), pre / 10))

            # Find the temperature closest to the current date.
            curr_date = datetime.now()
            date_temp = min([dt for dt in date_temp_list if dt[0] <= curr_date],
                            key=lambda t: abs(curr_date - t[0]))
            display_data.date_time = date_temp[0]
            display_data.temperature = date_temp[1]

            # Use the found date_time for dew point and precipitation.
            display_data.dew_point = next((dd[1] for dd in date_dew_list
                                           if dd[0] == date_temp[0]),
                                           float("nan"))
            display_data.precipitation = next((dp[1] for dp in date_pre_list
                                               if dp[0] == date_temp[0]),
                                               float("nan"))

        # Check whether days data is available.
        days_list = self.station_data.get(self.station.identifier, {}).get("days", [])
        if days_list:
            # Find the date in the days list closest to the current date.
            curr_date = datetime.now()
            day = min([da for da in days_list
                       if datetime.strptime(da["dayDate"], "%Y-%m-%d") <= curr_date],
                      key=lambda d: abs(curr_date -
                                        datetime.strptime(d["dayDate"], "%Y-%m-%d")))

            display_data.forecast = day["icon"]

            if day["temperatureMin"] >= -999 and day["temperatureMin"] <= 999:
                display_data.daily_min = day["temperatureMin"] / 10

            if day["temperatureMax"] >= -999 and day["temperatureMax"] <= 999:
                display_data.daily_max = day["temperatureMax"] / 10

        # Return all gathered data in a DisplayData object.
        return display_data
