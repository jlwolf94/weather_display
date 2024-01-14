"""
The start module contains the main function of the weather_display package
and can be used as an entry point script for the package.
"""

import sys

from weather_display.cli.argument_parser import create_argument_parser
from weather_display.cli.controller import Controller
from weather_display.cli.source import create_collector
from weather_display.displays.display import Display


def main():
    """
    Main function of the weather_display package and command line script.

    Returns:
        int: A successful run returns zero and all other runs return one.
    """
    parser = create_argument_parser()
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        return 1

    collector = create_collector(parser, args)
    display = _create_display(args)

    _start_display(display, collector)

    return 0


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
