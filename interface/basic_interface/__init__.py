import logging
import threading

# TODO: handle a failed connection


# Create Logger
LOGGER = logging.getLogger(__name__)
STOPPED = threading.Event()


def start():
    LOGGER.debug("Running the preloop-function, saying hi.")
    print("\n"
          "   ____    _    __  __    _    _   _ _____ _   _    _     ""\n"
          r"  / ___|  / \  |  \/  |  / \  | \ | |_   _| | | |  / \    ""\n"
          r"  \___ \ / _ \ | |\/| | / _ \ |  \| | | | | |_| | / _ \   ""\n"
          r"   ___) / ___ \| |  | |/ ___ \| |\  | | | |  _  |/ ___ \  ""\n"
          r"  |____/_/   \_\_|  |_/_/   \_\_| \_| |_| |_| |_/_/   \_\ ""\n"
          "                                                      hi~ ""\n"
          "  Starting up!\n")


def on_connect(response):
    print "$ Connected to the Server at {}\n$".format(response.peer)
    print "$ Please enter your command:"
    return


def on_open(comm_queue):
    worker = threading.Thread(target=get_input, args=(comm_queue,))
    worker.daemon = True
    worker.start()
    return


def message_sent(message):
    print "$ Message '{}' sent successfully.".format(message)


def on_message(payload, isBinary):
    if isBinary:
        print "$ Binary message received: {}".format(len(payload))
    else:
        print "$ Text message received: {}".format(payload.decode('utf8'))
    return


def on_exit():
    print "$ Received the command to close the connection."


def on_close(wasClean, code, reason):
    LOGGER.debug("Running the postloop-function, saying bye.")
    STOPPED.set()
    print("\n"
          "   ____    _    __  __    _    _   _ _____ _   _    _     ""\n"
          r"  / ___|  / \  |  \/  |  / \  | \ | |_   _| | | |  / \    ""\n"
          r"  \___ \ / _ \ | |\/| | / _ \ |  \| | | | | |_| | / _ \   ""\n"
          r"   ___) / ___ \| |  | |/ ___ \| |\  | | | |  _  |/ ___ \  ""\n"
          r"  |____/_/   \_\_|  |_/_/   \_\_| \_| |_| |_| |_/_/   \_\ ""\n"
          "                                                     bye~ ")


def print_msg(message):
    print "$ " + message


def get_input(comm_queue):
    while not STOPPED.is_set():
        comm_queue.put(raw_input().decode('utf8'))


if __name__ == "__main__":
    print ("This application is not meant to be executed on its own. To start "
           "it, please run '__main__.py' in it's parent directory, or the cli-"
           "command 'python interface' in the directory above (that should be "
           "'/PersonalAssistant_Interfaces').\n")
    var = raw_input("Press the enter-key to exit.\n")
