"""Starts the main interface. To be called with 'python interface'
from the root folder. After importing it, the interface will be
started start"""

import logging
import logging.handlers
import os.path
import time
import simple_cli as the_interface
import logger

try:
    import variables_private
except ImportError:
    variables_private = None
# The file variables_private.py is in my .gitignore - for good reasons.
# It includes private API-Keys that I don't want online. However, if you want
# to be able to send AutoRemote-Messages (see: http://joaoapps.com/autoremote/
# for certain log entries, create that file and add an entry called 'ar_key'
# for your private AutoRemote key (eg. "ar_key = 'YOUR_KEY_HERE'").


LOGGER = logging.getLogger(__name__)



if __name__ == '__main__':
    LOGGER.debug("-"*79)
    LOGGER.debug("Starting simple_cli")
    LOGGER.debug("-"*79)
    the_interface.start()
