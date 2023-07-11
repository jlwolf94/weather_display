"""
Main python file for the weather_display package that is executed when the
package is called directly through the python command `python -m weather_display`
from the parent directory.
"""

import argparse
import textwrap

from .dwd_stations import DwdStations
from .dwd_data import DwdData
from .display_data import DisplayData
from .display import Display


# Set up a parser for command line argument parsing.
parser = argparse.ArgumentParser(
    prog="weather_display",
    description=textwrap.dedent("""
        A simple Python program that retrieves weather data from different sources
        and displays the data on the console or on a display.
        """),
    epilog=textwrap.dedent("""
        Home page: <https://github.com/jlwolf94/weather_display/>
        Author: Jan-Lukas Wolf
        """),
    formatter_class=argparse.RawDescriptionHelpFormatter)

# Fill the parser with arguments.
parser.add_argument("-n", "--name", action="store", default="",
                    help="name of the weather station")
parser.add_argument("-x", "--lat", action="store", type=float,
                    help="geographic coordinate latitude")
parser.add_argument("-y", "--lon", action="store", type=float,
                    help="geographic coordinate longitude")
parser.add_argument("-v", "--version", action="version",
                    version="%(prog)s 1.0.0")

# Process the command line arguments.
args = parser.parse_args()

# Get the stations table.
dwd_stations = DwdStations()
dwd_stations.update()

# If latitude and longitude is available use the geographic coordinates.
if args.lat is not None and args.lon is not None:
    station_info = dwd_stations.get_station_info_by_distance(args.lat, args.lon)
else:
    station_info = dwd_stations.get_station_info_by_name(args.name)

# Get the station data.
dwd_data = DwdData(station_info)
dwd_data.update()

# Show the station data on the console.
display = Display()
display.show(dwd_data.get_display_data())
