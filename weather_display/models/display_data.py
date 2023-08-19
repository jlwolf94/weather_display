"""
The display_data module contains the DisplayData class that is used to store and
process the weather data that will be displayed by using the different methods
of the Display class. Additional it stores mapping dictionaries to convert
data to strings that are human readable.
"""


class DisplayData:
    """
    Class that contains the different parts of the weather data that will be
    displayed by the Display class methods. The data is gathered by the
    other Data classes available in the package. An additional mapping
    dictionary is stored as well.
    """

    DATE_FORMAT = ("%a., %d.%m.%Y", "Thu., 01.01.1970")
    """
    DATE_FORMAT (tuple[str, str]):
        A tuple defining the date format and default output string for the format.
    """

    TIME_FORMAT = ("%H:%M", "00:00")
    """
    TIME_FORMAT (tuple[str, str]):
        A tuple defining the time format and default output string for the format.
    """

    ICON_DICT = {1: "sun", 2: "sun, slightly cloudy", 3: "sun, cloudy", 4: "clouds",
                 5: "fog", 6: "fog, risk of slipping", 7: "light rain", 8: "rain",
                 9: "heavy rain", 10: "light rain, risk of slipping",
                 11: "heavy rain, risk of slipping", 12: "rain, sporadic snowfall",
                 13: "rain, increased snowfall", 14: "light snowfall", 15: "snowfall",
                 16: "heavy snowfall", 17: "clouds, hail", 18: "sun, light rain",
                 19: "sun, heavy rain", 20: "sun, rain, sporadic snowfall",
                 21: "sun, rain, increased snowfall", 22: "sun, sporadic snowfall",
                 23: "sun, increased snowfall", 24: "sun, hail", 25: "sun, heavy hail",
                 26: "thunderstorm", 27: "thunderstorm, rain",
                 28: "thunderstorm, heavy rain", 29: "thunderstorm, hail",
                 30: "thunderstorm, heavy hail", 31: "wind"
                }
    """
    ICON_DICT (dict[int, str]):
        A dictionary that contains the mapping of forecast icon numbers
        to human readable string representations.
    """

    def __init__(self, station_name="Error", date_time=None, temperature=float("nan"),
                 forecast=0, daily_min=float("nan"), daily_max=float("nan"),
                 dew_point=float("nan"), precipitation=float("nan")):
        """
        Constructor for the DisplayData objects.

        Parameters
        ----------
        station_name (str):
            Name of the weather station. Default value is Error.

        date_time (Optional[datetime]):
            A datetime object with the date and time of the provided
            weather data. Default value is None.

        temperature (float):
            The temperature in degree celsius. Default value is NAN.

        forecast (int):
            A number representing the weather forecast of the day.
            Default value is 0.

        daily_min (float):
            Minimum temperature of the day in degree celsius.
            Default value is NAN.

        daily_max (float):
            Maximum temperature of the day in degree celsius.
            Default value is NAN.

        dew_point (float):
            The dew point in degree celsius. Default value is NAN.

        precipitation (float):
            The current precipitation in millimeter.
            Default value is NAN.
        """

        self.station_name = station_name
        """
        station_name (str):
            Name of the weather station.
        """

        self.date_time = date_time
        """
        date_time (Optional[datetime]):
            A datetime object with the date and time of the provided
            weather data.
        """

        self.temperature = temperature
        """
        temperature (float):
            The temperature in degree celsius.
        """

        self.forecast = forecast
        """
        forecast (int):
            A number representing the weather forecast of the day.
        """

        self.daily_min = daily_min
        """
        daily_min (float):
            Minimum temperature of the day in degree celsius.
        """

        self.daily_max = daily_max
        """
        daily_max (float):
            Maximum temperature of the day in degree celsius.
        """

        self.dew_point = dew_point
        """
        dew_point (float):
            The dew point in degree celsius.
        """

        self.precipitation = precipitation
        """
        precipitation (float):
            The current precipitation in millimeter.
        """

    def get_formatted_date(self):
        """
        Method that uses the class constant DATE_FORMAT to convert the
        current datetime object to a formatted date string.

        Returns
        -------
        formatted_date (str):
            A formatted date representation of the datetime object.
        """

        return self.date_time.strftime(self.DATE_FORMAT[0]) \
            if self.date_time is not None else self.DATE_FORMAT[1]

    def get_formatted_time(self):
        """
        Method that uses the class constant TIME_FORMAT to convert the
        current datetime object to a formatted time string.

        Returns
        -------
        formatted_time (str):
            A formatted time representation of the datetime object.
        """

        return self.date_time.strftime(self.TIME_FORMAT[0]) \
            if self.date_time is not None else self.TIME_FORMAT[1]

    def get_formatted_forecast(self):
        """
        Method that converts the forecast number to a human readable string
        by using the ICON_DICT dictionary.

        Returns
        -------
        formatted_forecast (str):
            A formatted string representing the weather forecast of the day.
        """

        return self.ICON_DICT.get(self.forecast, "Error")
