"""
The controller module contains the Controller class that acts as the main
controller of the whole weather_display package. It bundles the data
collection and display control. The controller is thread safe and can only be
accessed by one thread at a time.
"""

import threading


class Controller:
    """
    The Controller class acts as the main controller of the whole
    weather_display package. It bundles the data collection and
    display control.
    """

    def __init__(self):
        """
        Constructor for the Controller objects.

        Parameters
        ----------
        collector (Collector):
            The configurated data collector of the program.

        display (Display):
            The virtual main display of the program.
        """

        self.lock = threading.Lock()
        """
        lock (Lock):
            The instance lock of a Controller class object.
        """
