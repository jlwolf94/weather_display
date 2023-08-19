"""
The start module contains the main function of the weather_display package
and can be used as an entry point script for the package.
"""

import sys
import argparse
import textwrap

from weather_display.models.display_data import DisplayData
from weather_display.models.station import Station
from weather_display.collectors.dwd_data import DwdData
from weather_display.collectors.w24_data import W24Data
from weather_display.dwd_stations import DwdStations
from weather_display.display import Display


def main():
    """
    Main function of the weather_display package and command line script.
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
    parser.add_argument("-i", "--id", action="store", type=int,
                        help="identifier of the weather station")
    parser.add_argument("-x", "--lat", action="store", type=float,
                        help="geographic coordinate latitude")
    parser.add_argument("-y", "--lon", action="store", type=float,
                        help="geographic coordinate longitude")
    parser.add_argument("-s", "--src", action="store", default=0,
                        type=int, help="number of the data source")
    parser.add_argument("-v", "--version", action="version",
                        version="%(prog)s 1.1.0")

    # Process the command line arguments.
    args = parser.parse_args()

    # Check for arguments and print the help if no arguments are present.
    if len(sys.argv) == 1:
        parser.print_help()
        return

    # Check which data source is selected.
    if args.src >= 1:
        # Initialize the display.
        display = Display()

        # Check whether a name and an identifier is present.
        if args.name == "Error" or args.id is None:
            # Show empty Data.
            display.show(DisplayData())
        else:
            # Get the station data.
            station = Station(name=args.name, number=args.id)
            w24_data = W24Data(station)
            w24_data.update()

            # Show the retrieved data.
            display.show(w24_data.get_display_data())
    else:
        # Get the stations table.
        dwd_stations = DwdStations()
        dwd_stations.update()

        # If latitude and longitude is available use the geographic coordinates.
        if args.lat is not None and args.lon is not None:
            station = dwd_stations.get_station_by_distance(args.lat, args.lon)
        else:
            station = dwd_stations.get_station_by_name(args.name)

        # Get the station data.
        dwd_data = DwdData(station)
        dwd_data.update()

        # Show the station data on the console.
        display = Display()
        display.show(dwd_data.get_display_data())


if __name__ == "__main__":
    sys.exit(main())
