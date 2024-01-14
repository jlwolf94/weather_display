"""
The output module contains functions to create and start the Display output.
The displayed data is gathered through the given Collector.
"""

from weather_display.cli.controller import Controller
from weather_display.displays.display import Display


def create_display(args):
    """
    The function creates a Display and configures it with the options
    set in the given arguments.

    Args:
        args (Namespace): The Namespace containing all arguments.

    Returns:
        Display: The configured virtual main display of the
            command line interface.
    """
    return Display(output=args.out, dark_mode=args.mode)


def start_display(display, collector):
    """
    The function shows the data from the Collector directly and exits or
    starts an external Controller that shows data from the Collector on
    the configured Display. The Controller enters an endless loop.

    Args:
        display (Display): The configured virtual main display of the
            command line interface.
        collector (Collector): The configured data Collector.
    """
    if display.output == Display.OUTPUTS[1]:
        controller = Controller(collector, display)
        controller.run()
    else:
        display.show(collector.get_display_data())
