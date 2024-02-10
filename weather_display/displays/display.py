"""
The display module contains the Display class that is responsible for displaying
weather data handed to its methods on the selected output channel.
The weather data is formatted to align with the chosen output channel.
The Display class imports all available displays for the output of data.
It functions as a virtual main display.
"""

from PIL import ImageFont

from weather_display.displays.lcd_144_controller import LCD144Controller
from weather_display.displays.util import is_raspberry_pi
from weather_display.models.data_image import DataImage


class Display:
    """
    Class that contains the configuration for different output channels.
    The methods of the class can be used to display DisplayData objects
    on the selected output channel with the set options.
    """

    OUTPUTS = (0, 1)
    """
    tuple[int, int]: A tuple containing the numbers of available output channels.
        Zero stands for the default console output.
    """

    def __init__(self, output=0, dark_mode=False):
        """
        Constructor for the Display objects.

        Args:
            output (int): A number representing the chosen output channel.
                Default value is 0 representing the console output.
            dark_mode (bool): A boolean that indicates whether the dark mode is
                active or not. The default value is False.
        """
        if output == self.OUTPUTS[1] and not is_raspberry_pi():
            output = 0
            print("Display Error: Output 1 can be used only on Raspberry Pi!")

        self.output = output if output in self.OUTPUTS else 0
        """
        int: A number representing the chosen output channel.
        """

        self.dark_mode = dark_mode
        """
        bool: A boolean that indicates whether the dark mode is active or not.
        """

        self.is_sleeping = False
        """
        bool: Sleeping status of the controlled display. The display starts in
            powered on mode by default.
        """

        self._font = self.load_default_font() if self.output == self.OUTPUTS[1] else None
        """
        FreeTypeFont, optional: The font used in the generation of Images.
            The default font is None.
        """

        self._lcd_con = LCD144Controller() if self.output == self.OUTPUTS[1] else None
        """
        LCD144Controller, optional: Controller of the 1.44inch LCD HAT SPI interface
            from Waveshare. The default controller is None.
        """

        self._event_detection_count = 0
        """
        int: Number of active event detections. The display starts with
            zero event detections.
        """

    @staticmethod
    def load_default_font():
        """
        Method that loads the set default font with a default font size.
        If the font can not be loaded then None is returned.

        Returns:
            FreeTypeFont, optional: The loaded font or None.
        """
        try:
            font = ImageFont.truetype(
                font="/usr/share/fonts/truetype/noto/NotoSansMono-Regular.ttf", size=10
            )
        except OSError as err_os:
            font = None
            print("Font Error:", err_os)

        return font

    def sleep(self, is_set):
        """
        Method that sets the sleep mode of the display to on or off.

        Args:
            is_set (bool): New status of the sleep mode that determinate whether
                it is on or off.
        """
        if self.output == self.OUTPUTS[1] and self._lcd_con is not None:
            if is_set != self.is_sleeping:
                self._lcd_con.sleep(is_set)
                self.is_sleeping = is_set

    def add_event_detection(self, callbacks):
        """
        Method that adds at most three callback functions to keys of the display.
        The keys are iterated from first to last.

        Args:
            callbacks (list[Any]): List of callback functions with at least
                one positional argument that will be used to register an event detection.
        """
        if self.output == self.OUTPUTS[1] and self._lcd_con is not None:
            for index, callback in enumerate(callbacks):
                if index == 0:
                    self._lcd_con.add_event_detect_key1(callback)
                elif index == 1:
                    self._lcd_con.add_event_detect_key2(callback)
                else:
                    self._lcd_con.add_event_detect_key3(callback)
                    break

            self._event_detection_count = len(callbacks) if len(callbacks) <= 3 else 3

    def remove_event_detection(self):
        """
        Method that removes at most three callback functions from the keys of the display.
        The key are iterated from first to last.
        """
        if self.output == self.OUTPUTS[1] and self._lcd_con is not None:
            for index in range(self._event_detection_count):
                if index == 0:
                    self._lcd_con.remove_event_detect_key1()
                elif index == 1:
                    self._lcd_con.remove_event_detect_key2()
                else:
                    self._lcd_con.remove_event_detect_key3()
                    break

            self._event_detection_count = 0

    @staticmethod
    def output_to_console(display_data):
        """
        Method that outputs the weather data contained in the DisplayData object
        to the console with the configured settings.

        Args:
            display_data (DisplayData): A DisplayData object containing all
                weather data to be shown on the console.
        """
        # Truncate station names that are too long.
        station_name = (
            (display_data.station_name[:35] + ".")
            if len(display_data.station_name) > 36
            else display_data.station_name
        )

        print(
            f"Station: {station_name}\n"
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
        to the display with the configured settings.

        Args:
            display_data (DisplayData): A DisplayData object containing all
                weather data to be shown on the display.
        """
        if self._lcd_con is not None:
            data_image = DataImage(display_data, self._font, self.dark_mode)
            self._lcd_con.show_image(
                data_image.create_data_image(self._lcd_con.width, self._lcd_con.height)
            )

    def show(self, display_data):
        """
        Method that tries to show the provided display_data on the configured
        output channel. The method automatically chooses the correct output function.

        Args:
            display_data (DisplayData): A DisplayData object containing all
                weather data to be shown on the configured output channel.
        """
        if display_data is None:
            return
        else:
            if self.output == self.OUTPUTS[1]:
                self.output_to_display(display_data)
            else:
                self.output_to_console(display_data)

    def exit(self):
        """
        Method that exits all used displays and controllers. The method
        performs the necessary cleanup actions to correctly exit the displays.
        """
        if self.output == self.OUTPUTS[1] and self._lcd_con is not None:
            self._lcd_con.cleanup()
