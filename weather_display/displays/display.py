"""
The display module contains the Display class that is responsible for displaying
weather data handed to the class or its methods on the selected output channel.
The weather data is formatted to align with the chosen output channel.
The Display class imports all available displays for the output of data.
It functions as a virtual main display.
"""

from PIL import Image, ImageFont, ImageDraw


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

    def __init__(self, output=0, dark_mode=False):
        """
        Constructor for the Display objects.

        Parameters
        ----------
        output (int):
            A number representing the chosen output channel.
            Default value is 0 representing the console output.

        dark_mode (bool):
            A boolean that indicates whether the dark mode is
            active or not. The default value is False.
        """

        self.output = output if output in self.OUTPUTS else 0
        """
        output (int):
            A number representing the chosen output channel.
        """

        self.dark_mode = dark_mode
        """
        dark_mode (bool):
            A boolean that indicates whether the dark mode is
            active or not.
        """

        self.font = None if output == self.OUTPUTS[0] else self.load_default_font()
        """
        font (Optional[Any]):
            The font used in the generation of images for the
            LCD display. The default font is None.
        """

    def load_default_font(self):
        """
        Method that loads the set default font with a default font size.
        If the font can not be loaded then None is returned.

        Returns
        -------
        font (Optional[Any]):
            The loaded font or None.
        """

        try:
            font = ImageFont.truetype(
                font="/usr/share/fonts/truetype/noto/NotoSansMono-Regular.ttf",
                size=10)
        except OSError as err_os:
            font = None
            print("Font Error:", err_os)

        return font

    def create_data_image_128_128(self, display_data):
        """
        Method that creates an image of 128 x 128 pixel that contains the data
        of the given DisplayData object.

        Parameters
        ----------
        display_data (DisplayData):
            A DisplayData object containing all weather data to be shown on
            the image.

        Returns
        -------
        image (Image):
            Created image that contains all data of the DisplayData object.
        """

        # Prepare image and color settings.
        image_mode = "RGB"
        image_size = (128, 128)
        if self.dark_mode:
            back_color = "BLACK"
            text_color = "WHITE"
        else:
            back_color = "WHITE"
            text_color = "BLACK"

        image = Image.new(mode=image_mode, size=image_size, color=back_color)
        draw = ImageDraw.Draw(image)

        # Truncate to long station names, forecasts and dates.
        station_name = (display_data.station_name[:16] + ".") \
            if len(display_data.station_name) > 17 else display_data.station_name
        formatted_forecast = display_data.get_formatted_forecast()
        forecast = (formatted_forecast[:9] + ".") \
            if len(formatted_forecast) > 10 else formatted_forecast
        date = display_data.get_formatted_date().split(" ")[1]

        # Draw image data.
        draw.text((10, 7), station_name, fill=text_color, font=self.font)
        draw.text((10, 21), f"{date}, {display_data.get_formatted_time()}",
                  fill=text_color, font=self.font)
        draw.text((10, 35), f"Fore.: {forecast}", fill=text_color, font=self.font)
        draw.text((10, 49), f"Tmax: {display_data.daily_max:5.1F} °C",
                  fill=text_color, font=self.font)
        draw.text((10, 63), f"Tmin: {display_data.daily_min:5.1F} °C",
                  fill=text_color, font=self.font)
        draw.text((10, 77), f"T:  {display_data.temperature:5.1F} °C",
                  fill=text_color, font=self.font)
        draw.text((10, 91), f"Td: {display_data.dew_point:5.1F} °C",
                  fill=text_color, font=self.font)
        draw.text((10, 105), f"Prec.: {display_data.precipitation:4.1F} mm",
                  fill=text_color, font=self.font)

        return image

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
        station_name = (display_data.station_name[:35] + ".") \
            if len(display_data.station_name) > 36 else display_data.station_name

        # Print the weather data to the console.
        print(f"Station: {station_name}\n"
              f"----------------------------------------------\n"
              f"Date: {display_data.get_formatted_date()}\n"
              f"Daily forecast: {display_data.get_formatted_forecast()}\n"
              f"Daily max. temp.: {display_data.daily_max:5.1F} °C\n"
              f"Daily min. temp.: {display_data.daily_min:5.1F} °C\n"
              f"----------------------------------------------\n"
              f"Time: {display_data.get_formatted_time()}\n"
              f"Temperature: {display_data.temperature:5.1F} °C\n"
              f"Dew point: {display_data.dew_point:5.1F} °C\n"
              f"Precipitation: {display_data.precipitation:4.1F} mm"
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

        # Create the image that will be shown on the display.
        image = self.create_data_image_128_128(display_data)

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
