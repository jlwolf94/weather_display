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


class LCD144Controller:
    """
    Class that is responsible for the management and direct control of the
    1.44inch LCD HAT SPI interface from Waveshare.
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
            print("LCD Error:", err_os)
            self.display = None
        except:
            print("LCD Error: Controller initialization failed!")
            self.display = None

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
