"""
The lcd_144_key_test module contains a main function that is used to test the
functionalities of the keys of the 1.44inch LCD HAT SPI interface from Waveshare.
"""

import sys
import RPi.GPIO as GPIO

from PIL import Image, ImageDraw, ImageFont, ImageColor
from weather_display.displays.lcd_144 import LCD144


def main():
    """
    Main function to test the keys of the 1.44inch LCD HAT SPI interface from Waveshare.
    """

    KEY_UP_PIN = 6
    KEY_DOWN_PIN = 19
    KEY_LEFT_PIN = 5
    KEY_RIGHT_PIN = 26
    KEY_PRESS_PIN = 13
    KEY1_PIN = 21
    KEY2_PIN = 20
    KEY3_PIN = 16

    # init GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()
    GPIO.setup(KEY_UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
    GPIO.setup(KEY_DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
    GPIO.setup(KEY_LEFT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
    GPIO.setup(KEY_RIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
    GPIO.setup(KEY_PRESS_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
    GPIO.setup(KEY1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
    GPIO.setup(KEY2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
    GPIO.setup(KEY3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up

    # Create LCD object for configuration and control.
    LCD = LCD144()

    # SCAN_DIR_DFT should be equal D2U_L2R
    scan_dir = 6
    LCD.init_LCD(scan_dir)
    LCD.clear()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = 128
    height = 128
    image = Image.new("RGB", (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    LCD.show_image(image)

    while True:
        if GPIO.input(KEY_UP_PIN) == 0:
            # button is released
            # up
            draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0xff00)
            print("up")
        else:
            # button is pressed
            # up filled
            draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0)

        if GPIO.input(KEY_LEFT_PIN) == 0:
            # button is released
            # left
            draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=0xff00)
            print("left")
        else:
            # button is pressed
            # left filled
            draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=0)

        if GPIO.input(KEY_RIGHT_PIN) == 0:
            # button is released
            # right
            draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=0xff00)
            print("right")
        else:
            # button is pressed
            # right filled
            draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=0)

        if GPIO.input(KEY_DOWN_PIN) == 0:
            # button is released
            # down
            draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0xff00)
            print("down")
        else:
            # button is pressed
            # down filled
            draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0)

        if GPIO.input(KEY_PRESS_PIN) == 0:
            # button is released
            # center
            draw.rectangle((20, 22, 40, 40), outline=255, fill=0xff00)
            print("center")
        else:
            # button is pressed
            # center filled
            draw.rectangle((20, 22, 40, 40), outline=255, fill=0)

        if GPIO.input(KEY1_PIN) == 0:
            # button is released
            # A button
            draw.ellipse((70, 0, 90, 20), outline=255, fill=0xff00)
            print("KEY1")
        else:
            # button is pressed
            # A button filled
            draw.ellipse((70, 0, 90, 20), outline=255, fill=0)

        if GPIO.input(KEY2_PIN) == 0:
            # button is released
            # B button
            draw.ellipse((100, 20, 120, 40), outline=255, fill=0xff00)
            print("KEY2")
        else:
            # button is pressed
            # B button filled
            draw.ellipse((100, 20, 120, 40), outline=255, fill=0)

        if GPIO.input(KEY3_PIN) == 0:
            # button is released
            # C button
            draw.ellipse((70, 40, 90, 60), outline=255, fill=0xff00)
            print("KEY3")
        else:
            # button is pressed
            # C button filled
            draw.ellipse((70, 40, 90, 60), outline=255, fill=0)

        LCD.show_image(image)


if __name__ == "__main__":
    sys.exit(main())
