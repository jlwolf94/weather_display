"""
The utils module contains utility functions for the displays sub-package.
"""

from pathlib import Path


def is_raspberry_pi():
    """
    Function that checks whether it is called on a Raspberry Pi or a
    different machine.

    Returns:
        bool: True if called on a Raspberry Pi and false in all other cases.
    """
    # The provided path is a symlink to the real configuration file.
    config_file_path = Path("/proc/device-tree/model")
    try:
        with config_file_path.open(mode="r") as file:
            if "raspberry pi" in file.read().lower():
                return True
            else:
                return False
    except OSError:
        return False
