"""
The controller module contains the Controller class that acts as the main
controller of the whole weather_display package. It bundles the data
collection and display control. The controller methods are thread safe
and can only be accessed by one thread at a time.
"""

import threading


class Controller:
    """
    The Controller class acts as the main controller of the whole
    weather_display package. It bundles the data collection and
    display control.
    """

    def __init__(self, collector, display, refresh=10):
        """
        Constructor for the Controller objects.

        Parameters
        ----------
        collector (Collector):
            The configurated data collector of the program.

        display (Display):
            The configurated virtual main display of the program.

        refresh (int):
            Refresh time for data collection and display in minutes.
            The default refresh time is 10 minutes.
        """

        self.collector = collector
        """
        collector (Collector):
            The configurated data collector of the program.
        """

        self.display = display
        """
        display (Display):
            The configurated virtual main display of the program.
        """

        self.refresh = refresh
        """
        refresh (int):
            Refresh time for data collection and display in minutes.
        """

        self.is_exited = False
        """
        is_exited (bool):
            Exit status of the controller. The start value is false and
            the status gets set to true when the exit method is called.
        """

        self.rlock = threading.RLock()
        """
        rlock (RLock):
            The reentrant lock of a Controller class object.
        """

    def activate_sleep(self):
        """
        Method that activates the sleep mode of the display. This method
        is thread safe.
        """

        with self.rlock:
            self.display.sleep(True)

    def update_and_show_data(self):
        """
        Method that updates the data using the collector methods and
        shows the updated data on the configurated display. This method is
        thread safe.
        """

        with self.rlock:
            display_data = self.collector.get_display_data()
            self.display.sleep(False)
            self.display.show(display_data)

    def exit(self):
        """
        Method that is called before leaving the Controller run method.
        It performs all necessary cleanup methods for the data collector
        and the display. This method is thread safe.
        """

        with self.rlock:
            self.display.remove_event_detection()
            self.display.exit()
            self.is_exited = True
