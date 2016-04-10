"""Starts the main interface. To be called with 'python interface'
from the root folder. After importing it, the interface will be
started start"""

import logging
import time
import simple_cli as the_interface
import variables_private


class AutoRemoteHandler(logging.Handler):
    """A Handler that sends logging messages to AutoRemote"""

    def emit(self, record):
        import requests
        logging.getLogger("requests").setLevel(logging.WARNING)
        message = self.format(record)
        # print "--- " + message + " ---"
        payload = {'key': variables_private.ar_key, 'message': message}
        requests.post("https://autoremotejoaomgcd.appspot.com/sendmessage",
                      payload)


class ColorStreamHandler(logging.StreamHandler):
    """A Handler that prints colored messages to the current console."""

    def emit(self, record):
        """
        This is the function that actually 'logs' the record. Here, it reads
        the part of the record containing the levelname (such as "DEBUG" or
        "ERROR") and adds ANSI-escape-codes around it to change the color.
        (see: http://ascii-table.com/ansi-escape-sequences.php)

        The String "DEBUG" will be replaced by "\033[96mDEBUG\033[0m" this way,
        in which "\033[" is the beginning, "m" the end of the escape sequence
        and 96 the actual Formatter, in this case the code for Cyan foreground
        text.

        If the levelname specified in the Formatter should have a specific
        length, this length is kept. If the levelname isn't part of the
        Formatter, nothing changes.

        After transforming the string inside the given record, the printing is
        handled via the original StreamHandler."""

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(self.level)
        stream_handler.setFormatter(self.formatter)

        # check if the levelname is even part of the current Formatter
        # if not, none of the transformations are necessary
        fmt = self.formatter._fmt
        if "levelname" in fmt:
            levelname = ""
            colors = {"DEBUG": "96",     # light cyan
                      "INFO": "97",      # white
                      "WARNING": "93",   # yellow
                      "ERROR": "91",     # red
                      "CRITICAL": "95"}  # magenta

            # find the actual part of the Formatter that formats the levelname
            fmt_placeholders = fmt.split(" ")
            for placeholder in fmt_placeholders:
                if "levelname" in placeholder:
                    # set a local variable to what the Formatter would have
                    # done. This is so that any changes to the string's length
                    # (e.g. exactly 8 with "%(levelname)-8s") are preserved.
                    levelname = placeholder % {"levelname": record.levelname}
            # replace the record's levelname with the modified version.
            record.levelname = "\033[{attr}m{lvlname}\033[0m".format(
                attr=colors[record.levelname],
                lvlname=levelname)
        logging.StreamHandler.emit(stream_handler, record)


def configure_logging():
    """Configure Logging. Add a streamhandler and a custom AutoRemoteHandler"""

    # create the logger
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    # create two formatter. They'll be used throughout the application.
    nice_formatter = logging.Formatter(
        "%(asctime)s %(levelname)-8s %(name)-12s %(message)s")
    full_formatter = logging.Formatter(
        "%(asctime)s %(levelname)-8s %(name)-12s %(message)s")
    practical_formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s",
        time.strftime("%X"))

    # create and add handlers
    file_handler = logging.FileHandler("interface.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(full_formatter)
    root.addHandler(file_handler)

    console_handler = ColorStreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(nice_formatter)
    # turned off for now, since I don't want the logging in my console.
    # root.addHandler(console_handler)

    autoremote_handler = AutoRemoteHandler()
    autoremote_handler.setLevel(logging.WARN)
    autoremote_handler.setFormatter(practical_formatter)
    root.addHandler(autoremote_handler)

# import os.path

# this_dir, this_filename = os.path.split(__file__)
# print this_dir
# print this_filename


if __name__ == '__main__':
    configure_logging()
    logging.debug("-"*79)
    logging.debug("Starting simple_cli")
    logging.debug("-"*79)
    the_interface.start()
