"""
The start module contains the main function of the weather_display package
and can be used as an entry point script for the package.
"""

import sys
import argparse
import textwrap

from weather_display.models.station import Station
from weather_display.collectors.stations_dwd import StationsDWD
from weather_display.collectors.collector import Collector
from weather_display.displays.display import Display
from weather_display.controller import Controller
from weather_display.utils import load_config_from_json


def get_argument_parser():
    """
    Method that builds and returns an argument parser that is setup
    to act as a CLI for the weather_display package.

    Returns
    -------
    parser (ArgumentParser):
        The configurated argument parser for the CLI.
    """

    # Set up a parser for command line argument parsing.
    parser = argparse.ArgumentParser(
        prog="weather_display",
        description=textwrap.dedent("""
            A simple Python program that retrieves weather data from different sources
            and displays the data on the console or on a display.
            """
        ),
        epilog=textwrap.dedent("""
            Home page: <https://github.com/jlwolf94/weather_display/>
            Author: Jan-Lukas Wolf
            """
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter)

    # Fill the parser with arguments.
    parser.add_argument("-n", "--name", action="store", default="Error",
                        help="name of the weather station")
    parser.add_argument("-i", "--id", action="store",
                        help="identifier of the weather station")
    parser.add_argument("-x", "--lat", action="store", type=float,
                        help="geographic coordinate latitude")
    parser.add_argument("-y", "--lon", action="store", type=float,
                        help="geographic coordinate longitude")
    parser.add_argument("-s", "--src", action="store", default=0,
                        type=int, help="number of the data source")
    parser.add_argument("-f", "--fil", action="store",
                        help="path to configuration file")
    parser.add_argument("-o", "--out", action="store", default=0,
                        type=int, help="number of the output channel")
    parser.add_argument("-m", "--mode", action="store_true",
                        help="dark mode setting for the output")
    parser.add_argument("-v", "--version", action="version",
                        version="%(prog)s 1.3.0")

    return parser

def get_station_from_args(source, args):
    """
    Method that creates a Station object with the given data source and
    options specified in the arguments.

    Parameters
    ----------
    source (str):
        Name or number of the selected data source.

    args (Namespace):
        A namespace created by the argument parser with all arguments.

    Returns
    -------
    station (Station):
        Created station with the set options.
    """

    # Create station with arguments for the selected data source.
    if source == Collector.SOURCES[1] or source == "1":
        try:
            converted_id = int(args.id)
        except TypeError:
            converted_id = 0
        except ValueError:
            converted_id = 0

        station = Station(name=args.name, number=converted_id)
    elif source == Collector.SOURCES[2] or source == "2":
        if args.id is not None:
            station = Station(name=args.name, identifier=args.id)
        else:
            station = Station(name=args.name)
    else:
        stations_dwd = StationsDWD()
        stations_dwd.update()

        if args.lat is not None and args.lon is not None:
            station = stations_dwd.get_station_by_distance(args.lat, args.lon)
        else:
            station = stations_dwd.get_station_by_name(args.name)

    return station

def main():
    """
    Main function of the weather_display package and command line script.

    Returns
    -------
    success (int):
        A successful run returns zero and all other runs return one.
    """

    # Get the argument parser and process the command line arguments.
    parser = get_argument_parser()
    args = parser.parse_args()

    # Check for arguments and print the help if no arguments are present.
    if len(sys.argv) == 1:
        parser.print_help()
        return 0

    # Configure the collector with a file configuration or the given arguments.
    if args.fil is not None:
        config = load_config_from_json(args.fil)
        stations = {}
        for source, options in config.items():
            station_args = parser.parse_args(options)
            station = get_station_from_args(str(source), station_args)
            stations.update({str(source): station})

        collector = Collector(stations)
    else:
        station = get_station_from_args(str(args.src), args)
        collector = Collector({str(args.src): station})

    # Configure the display and start the controller if necessary.
    display = Display(output=args.out, dark_mode=args.mode)
    if display.output == Display.OUTPUTS[1]:
        controller = Controller(collector, display)
        controller.run()
    else:
        display.show(collector.get_display_data())

    return 0


if __name__ == "__main__":
    sys.exit(main())
