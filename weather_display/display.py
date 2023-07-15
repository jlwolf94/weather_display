"""
The display module contains the Display class that is responsible for displaying
weather data handed to the class or its methods on the selected output channel.
The weather data is formatted to align with the chosen output channel.
"""


class Display:
    """
    Class that contains the configuration for different output channels.
    The methods of the class can be used to display DisplayData objects
    on the selected output channel with the set options.
    """

    OUTPUTS = (0, 1)
    """
    OUTPUTS (tuple[int, int]):
        A tuple containing the numbers of available output channels.
        Zero stands for the default console output.
    """

    COLOR_MODES = ("bw", "c")
    """
    COLOR_MODES (tuple[str, str]):
        A tuple containing strings that represent the accepted color modes.
        Two color modes are accepted in form of the black and white (bw) and
        color (c) color mode.
    """

    def __init__(self, output=0, width=128, height=128, color_mode="bw"):
        """
        Constructor for the Display objects.

        Parameters
        ----------
        output (int):
            A number representing the chosen output channel.
            Default value is 0 representing the console output.

        width (int):
            Width of the output display in pixels.
            The default value is 128 pixels.

        height (int):
            Height of the output display in pixels.
            The default value is 128 pixels.

        color_mode (str):
            A string that is part of the COLOR_MODES tuple and
            represent the black and white or color color mode.
            The default value is the black and white color mode (bw).
        """

        self.output = output if output in self.OUTPUTS else 0
        """
        output (int):
            A number representing the chosen output channel.
            Default value is 0 representing the console output.
        """

        self.width = width if width >= 0 and width <= 128 else 128
        """
        width (int):
            Width of the output display in pixels.
            The default value is 128 pixels.
        """

        self.height = height if height >= 0 and height <= 128 else 128
        """
        height (int):
            Height of the output display in pixels.
            The default value is 128 pixels.
        """

        self.color_mode = color_mode if color_mode in self.COLOR_MODES else "bw"
        """
        color_mode (str):
            A string that is part of the COLOR_MODES tuple and
            represent the black and white or color color mode.
            The default value is the black and white color mode (bw).
        """

    def output_to_console(self, display_data):
        """
        Method that outputs the weather data contained in the DisplayData object
        to the console with the configurated settings.

        Parameters
        ----------
        display_data (DisplayData):
            A DisplayData object containing all weather data to be shown on
            the console.
        """

        # Truncate station names that are to long.
        station_name = (display_data.station_name[:36] + ".") \
            if len(display_data.station_name) > 37 else display_data.station_name

        # Print the weather data to the console.
        print(f"Station: {station_name:37}    "
              f"Time: {display_data.formatted_time:20}    "
              f"Temperature: {display_data.temperature:5.1F} °C"
              "\n"
              f"Daily forecast: {display_data.formatted_forecast:30}    "
              f"Daily min. temp.: {display_data.daily_min:5.1F} °C    "
              f"Daily max. temp.: {display_data.daily_max:5.1F} °C"
             )

    def output_to_display(self, display_data):
        """
        Method that outputs the weather data contained in the DisplayData object
        to the display with the configurated settings.

        Parameters
        ----------
        display_data (DisplayData):
            A DisplayData object containing all weather data to be shown on
            the display.
        """

        pass

    def show(self, display_data):
        """
        Method that tries to show the provided display_data on the configurated
        output channel. The method automatically chooses the correct output function.

        Parameters
        ----------
        display_data (DisplayData):
            A DisplayData object containing all weather data to be shown on
            the configurated output channel.
        """

        # Check whether a DisplayData object is available.
        if display_data is None:
            return
        else:
            # Show the display_data.
            if self.output == self.OUTPUTS[1]:
                self.output_to_display(display_data)
            else:
                self.output_to_console(display_data)
