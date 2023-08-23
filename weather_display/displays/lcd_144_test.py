"""
The lcd_144_test module contains a main function that is used to test the
functionalities of the 1.44inch LCD HAT SPI interface from Waveshare.
"""

import RPi.GPIO as GPIO

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageColor
from weather_display.displays.lcd_144 import LCD144


def main():
    """
    Main function to test the 1.44inch LCD HAT SPI interface from Waveshare.

    Returns
    -------
    success (int):
        A successful run returns zero and all other runs return one.
    """

    try:
        # Create LCD object for configuration and control.
        LCD = LCD144()

        print("****init LCD****")
        # SCAN_DIR_DFT should be equal D2U_L2R
        scan_dir = 6
        LCD.init_LCD(scan_dir)
        LCD.clear()

        image = Image.new("RGB", (LCD.width, LCD.height), "WHITE")
        draw = ImageDraw.Draw(image)

        # font = ImageFont.truetype(
        #     "/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf", 16)

        print("****draw line****")
        draw.line([(0, 0), (127, 0)], fill="BLUE", width=5)
        draw.line([(127, 0), (127, 127)], fill="BLUE", width=5)
        draw.line([(127, 127), (0, 127)], fill="BLUE", width=5)
        draw.line([(0, 127), (0, 0)], fill="BLUE", width=5)

        print("****draw rectangle****")
        draw.rectangle([(18, 10), (110, 20)], fill="RED")

        print("****draw text****")
        draw.text((33, 22), "WaveShare ", fill="BLUE")
        draw.text((32, 36), "Electronic ", fill="BLUE")
        draw.text((28, 48), "1.44inch LCD ", fill="BLUE")

        # image.save(Path(__file__).parents[0].joinpath("test.png"))

        LCD.show_image(image)
        LCD.config.delay_driver_ms(500)

        image = Image.open(Path(__file__).parents[0].joinpath("sky.bmp"))
        LCD.show_image(image)

        return 0
    except:
        return 1
    finally:
        GPIO.cleanup()
