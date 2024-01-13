"""
The argument_parser module contains the all methods to create a ArgumentParser with
default settings. The ArgumentParser is the main object of the command line interface.
"""

import argparse
import textwrap


def create_argument_parser():
    """
    Function that creates an ArgumentParser with default settings.

    Returns:
        ArgumentParser: The ArgumentParser for the CLI with default settings.
    """
    parser = _create_argument_parser_with_default_settings()
    return _add_default_arguments(parser)


def _create_argument_parser_with_default_settings():
    return argparse.ArgumentParser(
        prog="weather_display",
        description=textwrap.dedent(
            """
            A simple Python program that retrieves weather data from different sources
            and displays the data on the console or on a display.
            """
        ),
        epilog=textwrap.dedent(
            """
            Home page: <https://github.com/jlwolf94/weather_display/>
            Author: Jan-Lukas Wolf
            """
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )


def _add_default_arguments(parser):
    parser.add_argument(
        "-n", "--name", action="store", default="Error", help="name of the weather station"
    )
    parser.add_argument("-i", "--id", action="store", help="identifier of the weather station")
    parser.add_argument(
        "-x", "--lat", action="store", type=float, help="geographic coordinate latitude"
    )
    parser.add_argument(
        "-y", "--lon", action="store", type=float, help="geographic coordinate longitude"
    )
    parser.add_argument(
        "-s", "--src", action="store", default=0, type=int, help="number of the data source"
    )
    parser.add_argument("-d", "--dir", action="store", help="path to config and data directory")
    parser.add_argument(
        "-o", "--out", action="store", default=0, type=int, help="number of the output channel"
    )
    parser.add_argument(
        "-m", "--mode", action="store_true", help="dark mode setting for the output"
    )
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.4.0")
    return parser
