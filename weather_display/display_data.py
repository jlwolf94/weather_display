"""
The display_data module contains the DisplayData class that is used to store and
process the weather data that will be displayed by using the different methods
of the Display class. Additional it stores mapping dictionaries to convert
data to strings that are human readable.
"""

import datetime


class DisplayData:
    """
    Class that contains the different parts of the weather data that will be
    displayed by the Display class methods. The data is gathered by the
    other Data classes available in the package. An additional mapping
    dictionary is stored as well.
    """

    TIME_FORMAT = ("%H:%M", "--:--")
    """
    TIME_FORMAT (tuple):
        A tuple defining the time format and default output for the format.
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
    ICON_DICT (dict):
        A dictionary that contains the mapping of forecast icon numbers
        to human readable string representations.
    """

    def __init__(self, station_name="Error", date_time=None, temperature=float("nan"),
                 forecast=0, daily_min=float("nan"), daily_max=float("nan")):
        """
        Constructor for the DisplayData objects.

        Parameters
        ----------
        station_name (str):
            Name of the weather station. Default value is Error.

        date_time (datetime):
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
        """

        self.station_name = station_name
        """
        station_name (str):
            Name of the weather station. Default value is Error.
        """

        self.date_time = date_time
        """
        date_time (datetime):
            A datetime object with the date and time of the provided
            weather data. Default value is None.
        """

        self.formatted_time = self.create_formatted_time(date_time)
        """
        formatted_time (str):
            A formatted representation of the date_time object.
        """

        self.temperature = temperature
        """
        temperature (float):
            The temperature in degree celsius. Default value is NAN.
        """

        self.forecast = forecast
        """
        forecast (int):
            A number representing the weather forecast of the day.
            Default value is 0.
        """

        self.formatted_forecast = self.create_formatted_forecast(forecast)
        """
        formatted_forecast (str):
            A formatted string representing the weather forecast of the day.
        """

        self.daily_min = daily_min
        """
        daily_min (float):
            Minimum temperature of the day in degree celsius.
            Default value is NAN.
        """

        self.daily_max = daily_max
        """
        daily_max (float):
            Maximum temperature of the day in degree celsius.
            Default value is NAN.
        """

    @classmethod
    def create_formatted_time(cls, dto):
        """
        Method that uses the class constant TIME_FORMAT to convert the
        given datetime object to formatted time string.

        Parameters
        ----------
        dto (datetime):
            A datetime object with the date and time of the provided
            weather data.

        Returns
        -------
        formatted_time (str):
            A formatted representation of the datetime object.
        """

        return dto.strftime(cls.TIME_FORMAT[0]) if dto is not None else cls.TIME_FORMAT[1]

    @classmethod
    def create_formatted_forecast(cls, forecast):
        """
        Method that converts the forecast number to a human readable string
        by using the ICON_DICT dictionary.

        Parameters
        ----------
        forecast (int):
            A number representing the weather forecast of the day.

        Returns
        -------
        formatted_forecast (str):
            A formatted string representing the weather forecast of the day.
        """

        return cls.ICON_DICT.get(forecast, "Error")
