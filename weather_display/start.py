"""
The start module contains the main function of the weather_display package
and can be used as an entry point script for the package.
"""

import argparse
import sys
import textwrap

from weather_display.collectors.collector import Collector
from weather_display.collectors.stations_dwd import StationsDWD
from weather_display.controller import Controller
from weather_display.displays.display import Display
from weather_display.models.station import Station
from weather_display.utils import get_data_directory, load_config_from_json


def main():
    """
    Main function of the weather_display package and command line script.

    Returns:
        int: A successful run returns zero and all other runs return one.
    """
    parser = _create_argument_parser()
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        return 1

    collector = _create_collector(parser, args)
    display = _create_display(args)

    _start_display(display, collector)

    return 0


def _create_argument_parser():
    parser = _create_argument_parser_with_default_settings()
    _add_default_arguments_to_argument_parser(parser)
    return parser


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


def _add_default_arguments_to_argument_parser(parser):
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


def _create_collector(parser, args):
    if args.dir is not None:
        collector = _create_collector_from_file_configuration(parser, args)
    else:
        collector = _create_collector_from_arguments(args)

    return collector


def _create_collector_from_file_configuration(parser, args):
    data_directory = get_data_directory(args.dir)
    config = load_config_from_json(data_directory)
    stations = {}

    for source, options in config.items():
        station_args = parser.parse_args(options)
        station = create_station_from_arguments(str(source), station_args, data_directory)
        stations.update({str(source): station})

    return Collector(stations)


def _create_collector_from_arguments(args):
    station = create_station_from_arguments(str(args.src), args)
    return Collector({str(args.src): station})


def create_station_from_arguments(source, args, data_directory=None):
    """
    Method that creates a Station object with the given data source, options specified in
    the arguments and data directory.

    Args:
        source (str): Name or number of the selected data source.
        args (Namespace): A Namespace created by the ArgumentParser with all arguments.
        data_directory (Path, optional): The path to the config and data directory or None.

    Returns:
        Station: Created Station with the set options.
    """
    if source == Collector.SOURCES[1] or source == "1":
        station = _create_w24_station(args)
    elif source == Collector.SOURCES[2] or source == "2":
        station = _create_won_station(args)
    else:
        station = _create_dwd_station(args, data_directory)

    return station


def _create_w24_station(args):
    try:
        converted_id = int(args.id)
    except TypeError:
        converted_id = 0
    except ValueError:
        converted_id = 0

    return Station(name=args.name, number=converted_id)


def _create_won_station(args):
    if args.id is not None:
        station = Station(name=args.name, identifier=args.id)
    else:
        station = Station(name=args.name)

    return station


def _create_dwd_station(args, data_directory):
    stations_dwd = StationsDWD(data_directory=data_directory)
    stations_dwd.update()

    if args.lat is not None and args.lon is not None:
        station = stations_dwd.get_station_by_distance(args.lat, args.lon)
    else:
        station = stations_dwd.get_station_by_name(args.name)

    return station


def _create_display(args):
    return Display(output=args.out, dark_mode=args.mode)


def _start_display(display, collector):
    if display.output == Display.OUTPUTS[1]:
        controller = Controller(collector, display)
        controller.run()
    else:
        display.show(collector.get_display_data())


if __name__ == "__main__":
    sys.exit(main())
