"""
The source module contains functions to create the main data source in form of
the Collector class from a given ArgumentParser and the corresponding arguments.
"""

from weather_display.cli.configuration import create_data_directory, load_config_from_json
from weather_display.collectors.collector import Collector
from weather_display.collectors.stations_dwd import StationsDWD
from weather_display.models.station import Station


def create_collector(parser, args):
    """
    The function creates a data Collector with the information contained in
    the given ArgumentParser and arguments.

    Args:
        parser (ArgumentParser): The ArgumentParser used for the CLI.
        args (Namespace): The Namespace containing all arguments.

    Returns:
        Collector: The data Collector created with the station information in the arguments.
    """
    if args.dir is not None:
        collector = _create_collector_from_file_configuration(parser, args)
    else:
        collector = _create_collector_from_arguments(args)

    return collector


def _create_collector_from_file_configuration(parser, args):
    data_directory = create_data_directory(args.dir)
    config = load_config_from_json(data_directory)
    stations = {}

    for source, options in config.items():
        station_args = parser.parse_args(options)
        station = _create_station_from_arguments(str(source), station_args, data_directory)
        stations.update({str(source): station})

    return Collector(stations)


def _create_collector_from_arguments(args):
    station = _create_station_from_arguments(str(args.src), args)
    return Collector({str(args.src): station})


def _create_station_from_arguments(source, args, data_directory=None):
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
