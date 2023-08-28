"""
The lcd_144_test module contains a main function that is used to test the
functionalities of the 1.44inch LCD HAT SPI interface from Waveshare.
"""

from pathlib import Path
from PIL import Image, ImageDraw
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
        # Create LCD display object for configuration and control.
        display = LCD144()

        print("init LCD display")
        if display.init_LCD() == 1:
            return 1
        display.clear()

        # Create image to draw on.
        image = Image.new("RGB", (display.width, display.height), "WHITE")
        draw = ImageDraw.Draw(image)

        print("draw line")
        draw.line([(0, 0), (127, 0)], fill="BLUE", width=5)
        draw.line([(127, 0), (127, 127)], fill="BLUE", width=5)
        draw.line([(127, 127), (0, 127)], fill="BLUE", width=5)
        draw.line([(0, 127), (0, 0)], fill="BLUE", width=5)

        print("draw rectangle")
        draw.rectangle([(18, 10), (110, 20)], fill="RED")

        print("draw text")
        # font = ImageFont.truetype(
        #     "/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf", 16)
        draw.text((33, 22), "WaveShare ", fill="BLUE")
        draw.text((32, 36), "Electronic ", fill="BLUE")
        draw.text((28, 48), "1.44inch LCD ", fill="BLUE")

        # Save image and show it on the display.
        image.save(Path(__file__).parents[0].joinpath("test.png"))
        display.show_image(image)
        display.config.delay_driver_ms(500)

        # Open image and show it on the display.
        image = Image.open(Path(__file__).parents[0].joinpath("sky.bmp"))
        display.show_image(image)
        display.config.delay_driver_ms(500)

        print("test successful")
        return 0
    except:
        print("error during test")
        return 1
    finally:
        print("cleanup executed")
        LCD144.cleanup_GPIO()
