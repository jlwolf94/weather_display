"""
The controller module contains the Controller class that acts as the main
controller of the whole weather_display package. It bundles the data
collection and display control. The controller methods are thread safe
and can only be accessed by one thread at a time.
"""

import time
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

    def activate_sleep(self, channel=0):
        """
        Method that activates the sleep mode of the display. This method
        is thread safe.

        Parameters
        ----------
        channel (int):
            The channel that is wired to the pressed button.
            The default channel is zero.
        """

        with self.rlock:
            self.display.sleep(True)

    def update_and_show_data(self, channel=0):
        """
        Method that updates the data using the collector methods and
        shows the updated data on the configurated display. This method is
        thread safe.

        Parameters
        ----------
        channel (int):
            The channel that is wired to the pressed button.
            The default channel is zero.
        """

        with self.rlock:
            display_data = self.collector.get_display_data()
            self.display.sleep(False)
            self.display.show(display_data)

    def exit(self, channel=0):
        """
        Method that is called to initialize the exit of the controller.
        This method is thread safe.

        Parameters
        ----------
        channel (int):
            The channel that is wired to the pressed button.
            The default channel is zero.
        """

        with self.rlock:
            self.is_exited = True

    def run(self):
        """
        Main method of the Controller class that starts an endless loop
        that updates the data and display in the given refresh interval.
        This method is thread safe.
        """

        with self.rlock:
            # Update and show data for the first time.
            self.update_and_show_data()

            # Activate the event detection of the display buttons.
            self.display.add_event_detection([self.update_and_show_data,
                                              self.activate_sleep,
                                              self.exit])

            # Get a local copy of refresh.
            refresh = self.refresh

        while True:
            # Sleep until the next update is necessary.
            for index in range(60 * refresh):
                time.sleep(1.0)

                # Check every second whether the controller is exited.
                with self.rlock:
                    is_exited = self.is_exited

                if is_exited:
                    break

            # Update and show data or exit.
            with self.rlock:
                if self.is_exited:
                    self.display.remove_event_detection()
                    self.display.exit()
                    return

                if not self.display.is_sleeping:
                    self.update_and_show_data()
