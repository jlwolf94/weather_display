"""
The data_image module contains the DataImage class that is used to store DisplayData and
to generate different Images from the DisplayData that can be shown on a connected Display.
The font and a dark mode can be set at creation time.
"""

from PIL import Image, ImageDraw


class DataImage:
    """
    Class that stores the given DisplayData and offers methods to convert the
    stored DisplayData to different Images. The Image is build with the saved font
    and dark mode setting.
    """

    MIN_PIXEL_WIDTH = 128
    """
    int: Minimal width of the Image in pixel.
    """

    MIN_PIXEL_HEIGHT = 128
    """
    int: Minimal height of the Image in pixel.
    """

    def __init__(self, display_data, font=None, dark_mode=False):
        """
        Constructor for the DataImage objects.

        Args:
            display_data (DisplayData): The DisplayData object that contains all
                weather data that will be placed in the generated Images.
            font (FreeTypeFont, optional): The font used in the generation of Images.
                The default font is None.
            dark_mode (bool): A boolean that indicates whether the dark mode is
                active or not. The default value is False.
        """

        self.display_data = display_data
        """
        DisplayData: The DisplayData object that contains all weather data that
            will be placed in the generated Images.
        """

        self.font = font
        """
        FreeTypeFont: The font used in the generation of Images.
        """

        self.dark_mode = dark_mode
        """
        bool: A boolean that indicates whether the dark mode is active or not.
        """

    def create_data_image(self, width, height):
        """
        Method that generates an Image from the saved DisplayData with the given
        width, height and saved settings.

        Args:
            width (int): The width of the Image in pixel.
            height (int): The height of the Image in pixel.

        Returns:
            Image, optional: Created Image that contains all weather data of
                the saved DisplayData object.
        """
        if self.display_data is None:
            return None

        image_width = width if width >= self.MIN_PIXEL_WIDTH else self.MIN_PIXEL_WIDTH
        image_height = height if height >= self.MIN_PIXEL_HEIGHT else self.MIN_PIXEL_HEIGHT
        image_size = (image_width, image_height)

        return self._create_data_image(image_size)

    def _create_data_image(self, image_size):
        image_mode = "RGB"
        if self.dark_mode:
            back_color = "BLACK"
            text_color = "WHITE"
        else:
            back_color = "WHITE"
            text_color = "BLACK"
        image = Image.new(mode=image_mode, size=image_size, color=back_color)
        return self._draw_display_data_to_image(image, text_color)

    def _draw_display_data_to_image(self, image, text_color):
        draw = ImageDraw.Draw(image)
        pos_text_list = self._create_pos_text_list()

        for pos_text in pos_text_list:
            draw.text(xy=pos_text[0], text=pos_text[1], fill=text_color, font=self.font)

        return image

    def _create_pos_text_list(self):
        station_name, forecast, date = self._create_truncated_data()
        pos_text_list = [
            ((10, 7), str(station_name)),
            ((10, 21), f"{date}, {self.display_data.get_formatted_time()}"),
            ((10, 35), f"Fore.: {forecast}"),
            ((10, 49), f"Tmax: {self.display_data.daily_max:5.1F} °C"),
            ((10, 63), f"Tmin: {self.display_data.daily_min:5.1F} °C"),
            ((10, 77), f"T:  {self.display_data.temperature:5.1F} °C"),
            ((10, 91), f"Td: {self.display_data.dew_point:5.1F} °C"),
            ((10, 105), f"Prec.: {self.display_data.precipitation:4.1F} mm"),
        ]
        return pos_text_list

    def _create_truncated_data(self):
        station_name = (
            (self.display_data.station_name[:16] + ".")
            if len(self.display_data.station_name) > 17
            else self.display_data.station_name
        )
        formatted_forecast = self.display_data.get_formatted_forecast()
        forecast = (
            (formatted_forecast[:9] + ".") if len(formatted_forecast) > 10 else formatted_forecast
        )
        date = self.display_data.get_formatted_date().split(" ")[1]
        return station_name, forecast, date
