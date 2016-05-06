"""Starts the main interface. To be called with 'python interface'
from the root folder. After importing it, the interface will be
started start"""

from autobahn.twisted.websocket import WebSocketClientProtocol
import logging
import logging.handlers

import logger
import basic_interface as interface

try:
    import variables_private
except ImportError:
    variables_private = None
# The file variables_private.py is in my .gitignore - for good reasons.
# It includes private API-Keys that I don't want online. However, if you want
# to be able to send AutoRemote-Messages (see: http://joaoapps.com/autoremote/
# for certain log entries, create that file and add an entry called 'ar_key'
# for your private AutoRemote key (eg. "ar_key = 'YOUR_KEY_HERE'").


logger.initialize()
LOGGER = logging.getLogger(__name__)


class Interface(WebSocketClientProtocol):

    def onConnect(self, response):
        LOGGER.info("Server connected: %s", response.peer)
        interface.on_connect(response)

    def onOpen(self):
        # self.sendMessage(u"Hello, world!".encode('utf8'))
        # TODO Put some kind of authentication here
        interface.on_open()

        def sendInput():
            val = interface.get_input()
            if val == "exit":
                interface.on_exit()
                self.sendClose()
            else:
                self.sendMessage(val.encode('utf8'))
                interface.message_sent(val)
                self.factory.reactor.callLater(0.01, sendInput)

        self.factory.reactor.callLater(0.01, sendInput)

    def onMessage(self, payload, isBinary):
        if isBinary:
            LOGGER.info("Binary message received: %d", len(payload))
        else:
            LOGGER.info("Text message received: %s", payload.decode('utf8'))
        interface.on_message(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        if reason:
            LOGGER.info(reason)
        interface.on_close(wasClean, code, reason)
        reactor.stop()


if __name__ == '__main__':
    # TODO: Establish conection separately.
    LOGGER.debug("-"*79)
    LOGGER.debug("Starting Interface")
    LOGGER.debug("-"*79)
    interface.start()

    from twisted.internet import reactor

    from autobahn.twisted.websocket import WebSocketClientFactory
    factory = WebSocketClientFactory()
    factory.protocol = Interface

    reactor.connectTCP("127.0.0.1", 9000, factory)
    reactor.run()
