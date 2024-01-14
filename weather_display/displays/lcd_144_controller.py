"""
The lcd_144_controller module contains the LCD144Controller class that is
responsible for the management and direct control of the
1.44inch LCD HAT SPI interface from Waveshare. The Controller uses the LCD144
and LCD144Config class and defines additional callback functions.

MIT License

Copyright (C) July 16, 2018 Yehui from Waveshare

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documnetation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to  whom the Software is
furished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from weather_display.displays.lcd_144 import LCD144
from weather_display.displays.util import is_raspberry_pi
if is_raspberry_pi():
    import RPi.GPIO as GPIO


class LCD144Controller:
    """
    Class that is responsible for the management and direct control of the
    1.44inch LCD HAT SPI interface from Waveshare.
    """

    BOUNCETIME = 500
    """
    BOUNCETIME (int):
        Bouncetime of the switches next to the LCD display in ms.
        The time is used for software switch debouncing.
    """

    def __init__(self):
        """
        Constructor for the LCD144Controller objects.
        """

        self.display = None
        """
        display (Optional[LCD144]):
            LCD display object for configuration and control of the
            1.44inch LCD HAT SPI interface from Waveshare. The default
            value for failed initialization is None.
        """

        # Try to initialize the LCD display.
        try:
            self.display = LCD144()
            if self.display.init_LCD(with_keys=True) == 1:
                raise OSError("LCD initialization failed!")
            self.display.clear()
        except OSError as err_os:
            self.display = None
            print("LCD Error:", err_os)
        except:
            self.display = None
            print("LCD Error: Controller initialization failed!")

    def cleanup(self):
        """
        Method that clears the display and resets the GPIO pins
        to their default state. The default state is the configuration
        before the program started.
        """

        if self.display is not None:
            self.display.clear()
            self.display.cleanup_GPIO()
        else:
            LCD144.cleanup_GPIO()

    def sleep(self, is_set):
        """
        Method that sets the sleep mode of the LCD display.
        The method turns of the backligth and clears the display before
        setting it to sleep. The method activates the backlight again
        when sleep mode is exited.

        Parameters
        ----------
        is_set (bool):
            New status of the LCD sleep mode that determinates whether
            it is in or out sleep mode.
        """

        if self.display is not None:
            if is_set:
                self.display.set_backlight(False)
                self.display.clear()
                self.display.set_sleep(is_set)
            else:
                self.display.set_sleep(is_set)
                self.display.set_backlight(True)

    def add_event_detect(self, key, callback):
        """
        Method to add an event detection for a specified key
        with a given callback function.

        Parameters
        ----------
        key (int):
            Number of the pin that is connected to the key.

        callback (Any):
            Callback function to register with the set event.
        """

        try:
            if self.display is not None:
                GPIO.add_event_detect(key, GPIO.FALLING, callback=callback,
                                      bouncetime=self.BOUNCETIME)
            else:
                raise OSError("LCD display is not available!")
        except OSError as err_os:
            print("LCD Error:", err_os)

    def add_event_detect_KEY1(self, callback):
        """
        Method to add an event detection for KEY1 with a given
        callback function.

        Parameters
        ----------
        callback (Any):
            Callback function to register with the set event.
        """

        self.add_event_detect(key=self.display.config.KEY1_PIN,
                              callback=callback)

    def add_event_detect_KEY2(self, callback):
        """
        Method to add an event detection for KEY2 with a given
        callback function.

        Parameters
        ----------
        callback (Any):
            Callback function to register with the set event.
        """

        self.add_event_detect(key=self.display.config.KEY2_PIN,
                              callback=callback)

    def add_event_detect_KEY3(self, callback):
        """
        Method to add an event detection for KEY3 with a given
        callback function.

        Parameters
        ----------
        callback (Any):
            Callback function to register with the set event.
        """

        self.add_event_detect(key=self.display.config.KEY3_PIN,
                              callback=callback)

    def remove_event_detect(self, key):
        """
        Method to remove an event detection from a specified key.

        Parameters
        ----------
        key (int):
            Number of the pin that is connected to the key.
        """

        try:
            if self.display is not None:
                GPIO.remove_event_detect(key)
            else:
                raise OSError("LCD display is not available!")
        except OSError as err_os:
            print("LCD Error:", err_os)

    def remove_event_detect_KEY1(self):
        """
        Method to remove an event detection from KEY1.
        """

        self.remove_event_detect(self.display.config.KEY1_PIN)

    def remove_event_detect_KEY2(self):
        """
        Method to remove an event detection from KEY2.
        """

        self.remove_event_detect(self.display.config.KEY2_PIN)

    def remove_event_detect_KEY3(self):
        """
        Method to remove an event detection from KEY3.
        """

        self.remove_event_detect(self.display.config.KEY3_PIN)

    def show_image(self, image):
        """
        Method that shows an image on the display with the already
        configurated settings. If the image is not present nothing
        will be done.

        Parameters
        ----------
        image (Any):
            Image that will be shown on the display.
            The image needs to match the display size in pixel.
        """

        try:
            if self.display is not None:
                self.display.show_image(image)
            else:
                raise OSError("LCD display is not available!")
        except ValueError as err_val:
            print("Image Error:", err_val)
        except OSError as err_os:
            print("LCD Error:", err_os)
