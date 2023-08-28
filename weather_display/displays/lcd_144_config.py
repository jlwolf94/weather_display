"""
The lcd_144_config module contains the LCD144Config class that is responsible
for the basic configuration of the 1.44inch LCD HAT SPI interface from Waveshare.

LCD hardware interface implements (GPIO, SPI)

MIT License

Copyright (C) July 10, 2017 Yehui from Waveshare

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

import time
import spidev
import RPi.GPIO as GPIO


class LCD144Config:
    """
    Class that contains all constants and methods to configure the
    1.44inch LCD HAT SPI interface from Waveshare.
    """

    LCD_RST_PIN = 27
    """
    LCD_RST_PIN (int):
        LCD RST pin definition.
    """

    LCD_DC_PIN = 25
    """
    LCD_DC_PIN (int):
        LCD DC pin definition.
    """

    LCD_CS_PIN = 8
    """
    LCD_CS_PIN (int):
        LCD CS pin definition.
    """

    LCD_BL_PIN = 24
    """
    LCD_BL_PIN (int):
        LCD BL pin definition.
    """

    LCD_WIDTH = 128
    """
    LCD_WIDTH (int):
        Width of the display in pixel.
    """

    LCD_HEIGHT = 128
    """
    LCD_HEIGHT (int):
        Height of the display in pixel.
    """

    LCD_X = 2
    """
    LCD_X (int):
        Display adjustment in x-direction.
    """

    LCD_Y = 1
    """
    LCD_Y (int):
        Display adjustment in y-direction.
    """

    LCD_X_MAXPIXEL = 132
    """
    LCD_X_MAXPIXEL (int):
        Display width maximum memory in pixel.
    """

    LCD_Y_MAXPIXEL = 162
    """
    LCD_Y_MAXPIXEL (int):
        Display height maximum memory in pixel.
    """

    L2R_U2D = 1
    """
    L2R_U2D (int):
        Left to right, up to down scanning method.
    """

    L2R_D2U = 2
    """
    L2R_D2U (int):
        Left to right, down to up scanning method.
    """

    R2L_U2D = 3
    """
    R2L_U2D (int):
        Right to left, up to down scanning method.
    """

    R2L_D2U = 4
    """
    R2L_D2U (int):
        Right to left, down to up scanning method.
    """

    U2D_L2R = 5
    """
    U2D_L2R (int):
        Up to down, left to right scanning method.
    """

    U2D_R2L = 6
    """
    U2D_R2L (int):
        Up to down, right to left scanning method.
    """

    D2U_L2R = 7
    """
    D2U_L2R (int):
        Down to up, left to right scanning method.
    """

    D2U_R2L = 8
    """
    D2U_R2L (int):
        Down to up, right to left scanning method.
    """

    SCAN_DIR_DFT = 6
    """
    SCAN_DIR_DFT (int):
        Default scan direction.
    """

    def __init__(self):
        """
        Constructor for the LCD144Config object.
        """

        self.SPI = spidev.SpiDev(0, 0)
        """
        SPI (Any):
            SPI device with bus 0 and device 0.
        """

    def init_GPIO(self):
        """
        Method that initializes the GPIO object.

        Returns
        -------
        success (Optional[int]):
            On success 0 is returned and None in all other cases.
        """

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.LCD_RST_PIN, GPIO.OUT)
        GPIO.setup(self.LCD_DC_PIN, GPIO.OUT)
        GPIO.setup(self.LCD_CS_PIN, GPIO.OUT)
        GPIO.setup(self.LCD_BL_PIN, GPIO.OUT)
        self.SPI.max_speed_hz = 9000000
        self.SPI.mode = 0b00
        return 0

    def delay_driver_ms(self, delay):
        """
        Method that delays the driver execution by the given number
        of milliseconds.

        Parameters
        ----------
        delay (int):
            Number of milliseconds for the delay.
        """

        time.sleep(delay / 1000.0)

    def write_GPIO_output(self, pin, value):
        """
        Method that writes the given value to the given pin.

        Parameters
        ----------
        pin (int):
            Number of the addressed pin.

        value (int):
            Number that should be written on the pin.
        """

        GPIO.output(pin, value)

    def write_SPI_bytes(self, data):
        """
        Method that writes the given byte data to the SPI interface.

        Parameters
        ----------
        data (list[int]):
            Byte data that will be written to the SPI interface.
        """

        self.SPI.writebytes(data)
