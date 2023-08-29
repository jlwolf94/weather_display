"""
The utils module contains utility functions for the weather_display package.
"""

from pathlib import Path


def is_raspberry_pi():
    """
    Function that checks whether it is called on a Raspberry Pi or a
    different machine.

    Returns
    -------
    is_raspberry_pi (bool):
        True if called on a Raspberry Pi and False in all other cases.
    """

    # Get the path to the configuration file with the required information.
    # The provided path is a symlink to the real configuration file.
    file_path = Path("/proc/device-tree/model")
    try:
        with file_path.open(mode="r") as file:
            if "raspberry pi" in file.read().lower():
                return True
            else:
                return False
    except OSError:
        return False
