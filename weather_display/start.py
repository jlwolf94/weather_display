"""
The start module contains the main function of the weather_display package
and can be used as an entry point script for the package.
"""

import sys
import argparse
import textwrap
import weather_display.displays.lcd_144_test as lcd_144_test
import weather_display.displays.lcd_144_key_test as lcd_144_key_test

from weather_display.models.station import Station
from weather_display.collectors.dwd_stations import DwdStations
from weather_display.collectors.data_dwd import DataDWD
from weather_display.collectors.data_w24 import DataW24
from weather_display.collectors.data_won import DataWon
from weather_display.displays.display import Display
from weather_display.utils import is_raspberry_pi


def main():
    """
    Main function of the weather_display package and command line script.

    Returns
    -------
    success (int):
        A successful run returns zero and all other runs return one.
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
    parser.add_argument("-v", "--version", action="version",
                        version="%(prog)s 1.2.0")

    # Process the command line arguments.
    args = parser.parse_args()

    # Check for arguments and print the help if no arguments are present.
    if len(sys.argv) == 1:
        parser.print_help()
        return 0

    # Check which data source is selected.
    if args.src == 1:
        # Check whether an identifier is present and convertible.
        if args.id is not None:
            try:
                converted_id = int(args.id)
            except ValueError:
                converted_id = 0

            station = Station(name=args.name, number=converted_id)
        else:
            station = Station(name=args.name)

        # Get the station data.
        data_w24 = DataW24(station)
        data_w24.update()

        # Show the retrieved data.
        display = Display()
        display.show(data_w24.get_display_data())
    elif args.src == 2:
        # Check whether an identifier is present.
        if args.id is not None:
            station = Station(name=args.name, identifier=args.id)
        else:
            station = Station(name=args.name)

        # Get the station data.
        data_won = DataWon(station)
        data_won.update()

        # Show the retrieved data.
        display = Display()
        display.show(data_won.get_display_data())
    elif args.src == 3:
        if is_raspberry_pi():
            return lcd_144_test.main()
        else:
            print("Error: Can be used only on Raspberry Pi!")
            return 1
    elif args.src == 4:
        if is_raspberry_pi():
            return lcd_144_key_test.main()
        else:
            print("Error: Can be used only on Raspberry Pi!")
            return 1
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
        data_dwd = DataDWD(station)
        data_dwd.update()

        # Show the retrieved data.
        display = Display()
        display.show(data_dwd.get_display_data())

    return 0


if __name__ == "__main__":
    sys.exit(main())
