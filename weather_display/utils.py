"""
The utils module contains utility functions for the weather_display package.
"""

import json

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

def load_config_from_json(path):
    """
    Method that loads a configuration from a json file that is located at
    the given file path. The file needs to be a compatible json file.

    Parameters
    ----------
    path (str):
        The absolute path to the json file as a string.

    Returns
    -------
    config (dict[str, dict[str, str]]):
        A dictionary containing all configuration settings or an empty
        dictionary if no data could be loaded.
    """

    # Convert string to Path and check whether the file extension is correct.
    file_extension = ".json"
    if file_extension in path.lower():
        file_path = Path(path)
    else:
        file_path = Path(path + file_extension)

    # Try to load the configuration from the file.
    try:
        with file_path.open(encoding="utf-8") as file:
            return json.load(file)
    except OSError as err_os:
        print("I/O Error:", err_os)
        return {}
