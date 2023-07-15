"""
Main python file for the weather_display package that is executed when the
package is called directly through the python command `python -m weather_display`
from the parent directory.
"""

import sys

from weather_display.start import main


sys.exit(main())
