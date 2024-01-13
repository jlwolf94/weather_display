"""
The configuration module contains all methods used for the loading and processing
of configuration arguments and configuration files.
"""

import json

from pathlib import Path


def create_data_directory(path):
    """
    Method that checks whether the given string points to a usable config and
    data directory. It returns a constructed Path to the given data directory or to
    the created default data directory.

    Args:
        path (str): The path to a possible config and data directory.

    Returns:
        Path: A constructed Path object containing the path to the data directory.
    """
    try:
        data_directory = Path(path).resolve(strict=True)
        if data_directory.is_dir():
            return data_directory
        else:
            raise FileNotFoundError("Path is not a directory!")
    except (FileNotFoundError, RuntimeError) as err:
        print("I/O Error:", err)
        data_directory = Path.home().joinpath(".weather_display")
        data_directory.mkdir(parents=False, exist_ok=True)
        return data_directory


def load_config_from_json(data_directory):
    """
    Method that tries to load a configuration file from the directory
    given by the Path object. The default configuration file is named
    stations.json. The file needs to be a compatible json file in all cases.

    Args:
        data_directory (Path): The path to the config and data directory.

    Returns:
        dict[str, dict[str, str]]: A dictionary containing all configuration settings or
            an empty dictionary if no data could be loaded.
    """
    config_file_path = data_directory.joinpath("stations.json")
    if config_file_path.is_file():
        try:
            with config_file_path.open(encoding="utf-8") as file:
                return json.load(file)
        except OSError as err_os:
            print("I/O Error:", err_os)
            return {}
    else:
        print("I/O Error: File stations.json does not exist.")
        return {}
