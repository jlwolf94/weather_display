"""
The lcd_144 module contains the LCD144 class that is responsible for all input,
output and setting methods for the 1.44inch LCD HAT SPI interface from Waveshare.

Functions with the ST7735S chip driver to clear the screen, write, draw lines,
draw in general and to perform other functions.

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

import numpy as np

from weather_display.displays.lcd_144_config import LCD144Config
from weather_display.displays.util import is_raspberry_pi
if is_raspberry_pi():
    import RPi.GPIO as GPIO


class LCD144:
    """
    Class that is responsible for all input, output and setting methods
    for the 1.44inch LCD HAT SPI interface from Waveshare.
    """

    def __init__(self):
        """
        Constructor for the LCD144 objects.
        """

        self.config = LCD144Config()
        """
        config (LCD144Config):
            Configurations object for the display.
        """

        self.width = LCD144Config.LCD_WIDTH
        """
        width (int):
            Width of the display in pixel.
        """

        self.height = LCD144Config.LCD_HEIGHT
        """
        height (int):
            Height of the display in pixel.
        """

        self.scan_dir = LCD144Config.SCAN_DIR_DFT
        """
        scan_dir (int):
            Scan direction of the display.
        """

        self.x_adjust = LCD144Config.LCD_X
        """
        x_adjust (int):
            Adjustment in x-direction.
        """

        self.y_adjust = LCD144Config.LCD_Y
        """
        y_adjust (int):
            Adjustment in y-direction.
        """

    @staticmethod
    def cleanup_GPIO():
        """
        Method that calls the GPIO cleanup from the LCD144Config class.
        """

        LCD144Config.cleanup_gpio()

    def reset(self):
        """
        Method that performs a hardware reset.
        """

        GPIO.output(self.config.LCD_RST_PIN, GPIO.HIGH)
        self.config.delay_driver_ms(100)
        GPIO.output(self.config.LCD_RST_PIN, GPIO.LOW)
        self.config.delay_driver_ms(100)
        GPIO.output(self.config.LCD_RST_PIN, GPIO.HIGH)
        self.config.delay_driver_ms(100)

    def set_backlight(self, is_set):
        """
        Method that turns the LCD backlight on or off.

        Parameters
        ----------
        is_set (bool):
            New status of the backlight that determinates whether it is
            turned on or off.
        """

        if is_set:
            GPIO.output(self.config.LCD_BL_PIN, GPIO.HIGH)
        else:
            GPIO.output(self.config.LCD_BL_PIN, GPIO.LOW)

    def set_sleep(self, is_set):
        """
        Method that sets the sleep mode of the LCD to in or out.

        Parameters
        ----------
        is_set (bool):
            New status of the LCD sleep mode that determinates whether
            it is in or out sleep mode.
        """

        if is_set:
            self.write_reg(0x10)
        else:
            self.write_reg(0x11)

        self.config.delay_driver_ms(120)

    def read_key_input(self, key):
        """
        Method that returns the input value read from the given key.

        Parameters
        ----------
        key (int):
            Number of the pin that is connected to the key.

        Returns
        -------
        data (int):
            Data read from the given key pin.
        """

        return GPIO.input(key)

    def write_reg(self, reg):
        """
        Method that writes register data.

        Parameters
        ----------
        reg (int):
            Register data as an integer.
        """

        GPIO.output(self.config.LCD_DC_PIN, GPIO.LOW)
        self.config.write_spi_bytes([reg])

    def write_data_8bit(self, data):
        """
        Method that writes 8bit data.

        data (int):
            Byte data to write.
        """

        GPIO.output(self.config.LCD_DC_PIN, GPIO.HIGH)
        self.config.write_spi_bytes([data])

    def write_data_nlen_16bit(self, data, data_len):
        """
        Method that writes data with the given length.

        Parameters
        ----------
        data (int):
            Byte data to write.

        data_len (int):
            Length of the data.
        """

        GPIO.output(self.config.LCD_DC_PIN, GPIO.HIGH)
        for i in range(0, data_len):
            self.config.write_spi_bytes([data >> 8])
            self.config.write_spi_bytes([data & 0xff])

    def init_reg(self):
        """
        Method to initialize the common registers.
        """

        # ST7735R Frame Rate.
        self.write_reg(0xB1)
        self.write_data_8bit(0x01)
        self.write_data_8bit(0x2C)
        self.write_data_8bit(0x2D)

        self.write_reg(0xB2)
        self.write_data_8bit(0x01)
        self.write_data_8bit(0x2C)
        self.write_data_8bit(0x2D)

        self.write_reg(0xB3)
        self.write_data_8bit(0x01)
        self.write_data_8bit(0x2C)
        self.write_data_8bit(0x2D)
        self.write_data_8bit(0x01)
        self.write_data_8bit(0x2C)
        self.write_data_8bit(0x2D)

        # Column inversion.
        self.write_reg(0xB4)
        self.write_data_8bit(0x07)

        # ST7735R Power Sequence.
        self.write_reg(0xC0)
        self.write_data_8bit(0xA2)
        self.write_data_8bit(0x02)
        self.write_data_8bit(0x84)
        self.write_reg(0xC1)
        self.write_data_8bit(0xC5)

        self.write_reg(0xC2)
        self.write_data_8bit(0x0A)
        self.write_data_8bit(0x00)

        self.write_reg(0xC3)
        self.write_data_8bit(0x8A)
        self.write_data_8bit(0x2A)
        self.write_reg(0xC4)
        self.write_data_8bit(0x8A)
        self.write_data_8bit(0xEE)

        # VCOM.
        self.write_reg(0xC5)
        self.write_data_8bit(0x0E)

        # ST7735R Gamma Sequence.
        self.write_reg(0xe0)
        self.write_data_8bit(0x0f)
        self.write_data_8bit(0x1a)
        self.write_data_8bit(0x0f)
        self.write_data_8bit(0x18)
        self.write_data_8bit(0x2f)
        self.write_data_8bit(0x28)
        self.write_data_8bit(0x20)
        self.write_data_8bit(0x22)
        self.write_data_8bit(0x1f)
        self.write_data_8bit(0x1b)
        self.write_data_8bit(0x23)
        self.write_data_8bit(0x37)
        self.write_data_8bit(0x00)
        self.write_data_8bit(0x07)
        self.write_data_8bit(0x02)
        self.write_data_8bit(0x10)

        self.write_reg(0xe1)
        self.write_data_8bit(0x0f)
        self.write_data_8bit(0x1b)
        self.write_data_8bit(0x0f)
        self.write_data_8bit(0x17)
        self.write_data_8bit(0x33)
        self.write_data_8bit(0x2c)
        self.write_data_8bit(0x29)
        self.write_data_8bit(0x2e)
        self.write_data_8bit(0x30)
        self.write_data_8bit(0x30)
        self.write_data_8bit(0x39)
        self.write_data_8bit(0x3f)
        self.write_data_8bit(0x00)
        self.write_data_8bit(0x07)
        self.write_data_8bit(0x03)
        self.write_data_8bit(0x10)

        # Enable test command.
        self.write_reg(0xF0)
        self.write_data_8bit(0x01)

        # Disable ram power save mode.
        self.write_reg(0xF6)
        self.write_data_8bit(0x00)

        # 65k mode.
        self.write_reg(0x3A)
        self.write_data_8bit(0x05)

    def set_gram_scan_way(self, scan_dir):
        """
        Method that sets the display scan direction.

        Parameters
        ----------
        scan_dir (int):
            Number for the new scan direction.
        """

        # Save the new screen scan direction.
        self.scan_dir = scan_dir

        # Get GRAM and LCD width and height.
        if ((scan_dir == self.config.L2R_U2D) or (scan_dir == self.config.L2R_D2U)
            or (scan_dir == self.config.R2L_U2D) or (scan_dir == self.config.R2L_D2U)):
            self.width = self.config.LCD_HEIGHT
            self.height = self.config.LCD_WIDTH
            if scan_dir == self.config.L2R_U2D:
                memory_access_reg_data = 0X00 | 0x00
            elif scan_dir == self.config.L2R_D2U:
                memory_access_reg_data = 0X00 | 0x80
            elif scan_dir == self.config.R2L_U2D:
                memory_access_reg_data = 0x40 | 0x00
            else:
                # R2L_D2U:
                memory_access_reg_data = 0x40 | 0x80
        else:
            self.width = self.config.LCD_WIDTH
            self.height = self.config.LCD_HEIGHT
            if scan_dir == self.config.U2D_L2R:
                memory_access_reg_data = 0X00 | 0x00 | 0x20
            elif scan_dir == self.config.U2D_R2L:
                memory_access_reg_data = 0X00 | 0x40 | 0x20
            elif scan_dir == self.config.D2U_L2R:
                memory_access_reg_data = 0x80 | 0x00 | 0x20
            else:
                # D2U_R2L:
                memory_access_reg_data = 0x40 | 0x80 | 0x20

        # Please set (memory_access_reg_data & 0x10) != 1.
        if (memory_access_reg_data & 0x10) != 1:
            self.x_adjust = self.config.LCD_Y
            self.y_adjust = self.config.LCD_X
        else:
            self.x_adjust = self.config.LCD_X
            self.y_adjust = self.config.LCD_Y

        # Set the read and write scan direction of the frame memory with
        # MX, MY, RGB mode and 0x08 set RGB.
        self.write_reg(0x36)
        self.write_data_8bit(memory_access_reg_data | 0x08)

    def init_LCD(self, scan_dir=LCD144Config.SCAN_DIR_DFT,
                 with_warnings=False, with_keys=False):
        """
        Method that initializes the whole display with the given scan direction
        and activation state of warnings and keys.

        Parameters
        ----------
        scan_dir (int):
            Number for the new scan direction.
            Default value is the default scan direction from the config class.

        with_warnings (bool):
            Sets whether warnings are displayed on the console.
            Default value is False.

        with_keys (bool):
            Sets whether the keys of the display should be initialized.
            Default value is False.

        Returns
        -------
        success (Optional[int]):
            On failure one is returned and None in all other cases.
        """

        # Try to initialize the GPIO pins.
        if self.config.init_gpio(with_warnings=with_warnings,
                                 with_keys=with_keys) != 0:
            return 1

        # Turn on the backlight.
        self.set_backlight(True)

        # Hardware reset.
        self.reset()

        # Set the initialization register.
        self.init_reg()

        # Set the display scan and color transfer modes.
        self.set_gram_scan_way(scan_dir)
        self.config.delay_driver_ms(200)

        # Sleep mode out.
        self.set_sleep(False)

        # Turn on the LCD display.
        self.write_reg(0x29)

    def set_windows(self, x_start, y_start, x_end, y_end):
        """
        Method that sets the start and end position of the display area.

        Parameters
        ----------
        x_start (int):
            Start position in x-direction.

        y_start (int):
            Start position in y-direction.

        x_end (int):
            End position in x-direction.

        y_end (int):
            End position in y-direction.
        """

        # Set the x-coordinates.
        self.write_reg(0x2A)
        self.write_data_8bit(0x00)
        self.write_data_8bit((x_start & 0xff) + self.x_adjust)
        self.write_data_8bit(0x00)
        self.write_data_8bit(((x_end - 1) & 0xff) + self.x_adjust)

        # Set the y-coordinates.
        self.write_reg(0x2B)
        self.write_data_8bit(0x00)
        self.write_data_8bit((y_start & 0xff) + self.y_adjust)
        self.write_data_8bit(0x00)
        self.write_data_8bit(((y_end - 1) & 0xff) + self.y_adjust)

        self.write_reg(0x2C)

    def clear(self):
        """
        Method that clears the display.
        """

        buffer = [0xff] * (self.width * self.height * 2)
        self.set_windows(0, 0, self.width, self.height)
        GPIO.output(self.config.LCD_DC_PIN, GPIO.HIGH)
        for i in range(0, len(buffer), 4096):
            self.config.write_spi_bytes(buffer[i:i + 4096])

    def show_image(self, image):
        """
        Method that shows an image on the display with the already configurated
        settings.

        Parameters
        ----------
        image (Any):
            Image that will be shown on the display.
            The image needs to match the display size in pixel.
        """

        # Check whether an image exists.
        if image is None:
            return

        # Get the image dimensions and compare them with the display size.
        img_width, img_height = image.size
        if img_width != self.width or img_height != self.height:
            raise ValueError(
                f"Image must be same dimensions as the display ({self.width}x{self.height}).")

        img = np.asarray(image)
        pix = np.zeros((self.width, self.height, 2), dtype=np.uint8)
        pix[..., [0]] = np.add(np.bitwise_and(img[..., [0]], 0xF8),
                               np.right_shift(img[..., [1]], 5))
        pix[..., [1]] = np.add(np.bitwise_and(np.left_shift(img[..., [1]], 3), 0xE0),
                               np.right_shift(img[..., [2]], 3))
        pix = pix.flatten().tolist()

        self.set_windows(0, 0, self.width, self.height)
        GPIO.output(self.config.LCD_DC_PIN, GPIO.HIGH)
        for i in range(0, len(pix), 4096):
            self.config.write_spi_bytes(pix[i:i + 4096])
