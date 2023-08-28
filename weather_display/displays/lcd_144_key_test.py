"""
The lcd_144_key_test module contains a main function that is used to test the
functionalities of the keys of the 1.44inch LCD HAT SPI interface from Waveshare.
"""

from PIL import Image, ImageDraw
from weather_display.displays.lcd_144 import LCD144


def main():
    """
    Main function to test the keys of the 1.44inch LCD HAT SPI interface from Waveshare.

    Returns
    -------
    success (int):
        A successful run returns zero and all other runs return one.
    """

    try:
        # Create LCD display object for configuration and control.
        display = LCD144()

        print("init LCD display")
        if display.init_LCD(with_keys=True) == 1:
            return 1
        display.clear()

        # Create blank image for drawing.
        image = Image.new("RGB", (display.width, display.height))
        draw = ImageDraw.Draw(image)

        # Draw a black filled box to clear the image.
        print("draw rectangle")
        draw.rectangle((0, 0, display.width, display.height), outline=0, fill=0)
        display.show_image(image)

        # Wait for user input.
        print("wait for user input")
        while True:
            if display.read_key_input(display.config.KEY_UP_PIN) == 0:
                # button is released
                # up
                draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0xff00)
                print("up")
            else:
                # button is pressed
                # up filled
                draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0)

            if display.read_key_input(display.config.KEY_LEFT_PIN) == 0:
                # button is released
                # left
                draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=0xff00)
                print("left")
            else:
                # button is pressed
                # left filled
                draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=0)

            if display.read_key_input(display.config.KEY_RIGHT_PIN) == 0:
                # button is released
                # right
                draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=0xff00)
                print("right")
            else:
                # button is pressed
                # right filled
                draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=0)

            if display.read_key_input(display.config.KEY_DOWN_PIN) == 0:
                # button is released
                # down
                draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0xff00)
                print("down")
            else:
                # button is pressed
                # down filled
                draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0)

            if display.read_key_input(display.config.KEY_PRESS_PIN) == 0:
                # button is released
                # center
                draw.rectangle((20, 22, 40, 40), outline=255, fill=0xff00)
                print("center")
            else:
                # button is pressed
                # center filled
                draw.rectangle((20, 22, 40, 40), outline=255, fill=0)

            if display.read_key_input(display.config.KEY1_PIN) == 0:
                # button is released
                # A button
                draw.ellipse((70, 0, 90, 20), outline=255, fill=0xff00)
                print("KEY1")
            else:
                # button is pressed
                # A button filled
                draw.ellipse((70, 0, 90, 20), outline=255, fill=0)

            if display.read_key_input(display.config.KEY2_PIN) == 0:
                # button is released
                # B button
                draw.ellipse((100, 20, 120, 40), outline=255, fill=0xff00)
                print("KEY2")
            else:
                # button is pressed
                # B button filled
                draw.ellipse((100, 20, 120, 40), outline=255, fill=0)

            if display.read_key_input(display.config.KEY3_PIN) == 0:
                # button is released
                # C button
                draw.ellipse((70, 40, 90, 60), outline=255, fill=0xff00)
                print("KEY3")
            else:
                # button is pressed
                # C button filled
                draw.ellipse((70, 40, 90, 60), outline=255, fill=0)

            display.show_image(image)
    except:
        print("error during test")
        return 1
    finally:
        print("cleanup executed")
        LCD144.cleanup_GPIO()
