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

def is_possible_data_directory(path):
    """
    Method that check whether the given path points to a usable config and
    data directory or not.

    Parameters
    ----------
    path (str):
        The path to a possible config and data directory.

    Returns
    -------
    is_possible_data_directory (bool):
        Indicates whether the path is a possible directory or not.
    """

    # Try to convert the string to an absolute path.
    try:
        data_directory = Path(path).resolve(strict=True)
        if data_directory.is_dir():
            return True
        else:
            raise FileNotFoundError("Path is not a directory!")
    except (FileNotFoundError, RuntimeError) as err:
        print("I/O Error:", err)
        return False

def load_config_from_json(path):
    """
    Method that tries to load a configuration file from the directory
    given by path. The default configuration file is named stations.json.
    The file needs to be a compatible json file in all cases.

    Parameters
    ----------
    path (str):
        The path to the config and data directory where the stations.json
        file is located.

    Returns
    -------
    config (dict[str, dict[str, str]]):
        A dictionary containing all configuration settings or an empty
        dictionary if no data could be loaded.
    """

    # Try to convert the string to an absolute path.
    if is_possible_data_directory(path):
        data_directory = Path(path).resolve(strict=True)
    else:
        # Fall back to default data directory.
        data_directory = Path.home().joinpath(".weather_display")
        data_directory.mkdir(parents=False, exist_ok=True)

    # Search for the config file and try to read it.
    file_path = data_directory.joinpath("stations.json")
    if file_path.is_file():
        try:
            with file_path.open(encoding="utf-8") as file:
                return json.load(file)
        except OSError as err_os:
            print("I/O Error:", err_os)
            return {}
    else:
        print("I/O Error: File stations.json does not exist.")
        return {}
