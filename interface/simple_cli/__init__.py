"""A simple command line interface.
It attempts to connect to a server, by default on the current machine
and then allows the user to enter commands"""
import cmd
import logging
import requests

# Create Logger
LOGGER = logging.getLogger(__name__)


class CommandLineInterface(cmd.Cmd):
    """A simple implementation of a CLI"""

    connection = {"url": "localhost", "port": 9000}
    connection_attempts = 0
    prompt = ">>> "

    def preloop(self):
        """Runs before the loop. Greets the user"""
        LOGGER.debug("Running the preloop-function, saying hi.")
        print("\n"
              "   ____    _    __  __    _    _   _ _____ _   _    _     ""\n"
              r"  / ___|  / \  |  \/  |  / \  | \ | |_   _| | | |  / \    ""\n"
              r"  \___ \ / _ \ | |\/| | / _ \ |  \| | | | | |_| | / _ \   ""\n"
              r"   ___) / ___ \| |  | |/ ___ \| |\  | | | |  _  |/ ___ \  ""\n"
              r"  |____/_/   \_\_|  |_/_/   \_\_| \_| |_| |_| |_/_/   \_\ ""\n"
              "                                                      hi~ ""\n"
              "  Starting up!\n")
        self.connect()

    def postloop(self):
        """Runs after the loop."""
        LOGGER.debug("Running the postloop-function, saying bye.")
        print("\n"
              "   ____    _    __  __    _    _   _ _____ _   _    _     ""\n"
              r"  / ___|  / \  |  \/  |  / \  | \ | |_   _| | | |  / \    ""\n"
              r"  \___ \ / _ \ | |\/| | / _ \ |  \| | | | | |_| | / _ \   ""\n"
              r"   ___) / ___ \| |  | |/ ___ \| |\  | | | |  _  |/ ___ \  ""\n"
              r"  |____/_/   \_\_|  |_/_/   \_\_| \_| |_| |_| |_/_/   \_\ ""\n"
              "                                                     bye~ ")

    def parseline(self, line):
        """Parses a line
        TODO: actually send the command to the server."""
        LOGGER.debug("Parsing '%s'.", line)
        ret = cmd.Cmd.parseline(self, line)
        try:
            LOGGER.info("Attempting to send '%s' to the server.", ret)
            requests.post("http://{url}:{port}/command"
                          .format(**self.connection),
                          {"key": ret[0], "params": ret[1], "comm": ret[2]})
        except requests.ConnectionError:
            LOGGER.error("Connection lost.")
            print "Connection lost."
            self.connection_error()
            return ("exit", "", "exit")
        print "processing " + str(ret)
        return ret

    def emptyline(self):
        pass

    def default(self, line):
        pass

    def precmd(self, line):
        LOGGER.debug("Running the precmd-function")
        return cmd.Cmd.precmd(self, line)

    def postcmd(self, stop, line):
        LOGGER.debug("Running the postcmd-function")
        return cmd.Cmd.postcmd(self, stop, line)

    def do_EOF(self, line):
        """Exit the interface"""
        return self.do_exit(line)

    def do_exit(self, line):
        """Exit the interface"""
        LOGGER.info("Received the command '%s'. Exiting", line)
        return True

    def connect(self):
        """attept connecting to an instance of Samantha"""
        LOGGER.info("Attempting to connect to 'http://%(url)s:%(port)s'",
                    self.connection)
        print("Attempting to connect to 'http://{url}:{port}'"
              .format(**self.connection))
        try:
            requests.get("http://{url}:{port}/status"
                         .format(**self.connection))
            self.connection_attempts = 0
            LOGGER.info("Connection successful. "
                        "Connection-attempts reset to 0.")
            print "Connection available."
        except requests.ConnectionError:
            LOGGER.error("Could not connect!")
            self.connection_error()

    def connection_error(self):
        """Handle a failed connection. The program will abort after 3
        failed attempts to the same server."""
        self.connection_attempts += 1
        if self.connection_attempts >= 3:
            LOGGER.fatal("Couldn't connect 3 times in a row. Exiting.")
            print "The connection failed 3 times in a row. Exiting."
            self.postloop()
            exit()
        LOGGER.info("Connection failed. Attempt(%d/3)",
                    self.connection_attempts)
        print("The Connection to 'http://{url}:{port}/status' failed."
              .format(**self.connection))
        LOGGER.debug("Requiring userinput whether to try starting the server "
                     "manually.")
        var = raw_input("Try to start the server remotely? (y/n) \n>>> ")
        LOGGER.debug("Userinput was '%s'.", var)
        while var not in ["y", "n"]:
            var = raw_input("Please use 'y' for yes or 'n' for no. \n>>> ")
        if var == "y":
            LOGGER.info("Attempting to start the Server remotely.")
            # TODO Start the server remotely
        elif var == "n":
            LOGGER.debug("Requiring userinput whether to change the server's "
                         "address.")
            var = raw_input("Enter a new host? (y/n) \n>>> ")
            LOGGER.debug("Userinput was '%s'.", var)
            while var not in ["y", "n"]:
                var = raw_input(
                    "Please use 'y' for yes or 'n' for no. \n>>> ")
            if var == "y":
                self.connection_attempts = 0
                self.connection["url"] = raw_input(
                    "Please enter the new host: ")
                LOGGER.info("Address changed to '%s'. Connection-attempts "
                            "reset to 0", self.connection["url"])
        LOGGER.info("Attempting to reconnect.")
        self.connect()


def start():
    """Starts the interface"""
    CommandLineInterface().cmdloop("Please enter your command:")

if __name__ == "__main__":
    print ("This application is not meant to be executed on its own. To start "
           "it, please run '__main__.py' in it's parent directory, or the cli-"
           "command 'python interface' in the directory above (that should be "
           "'/PersonalAssistant_Interfaces').\n")
    var = raw_input("Press the enter-key to exit.\n")
