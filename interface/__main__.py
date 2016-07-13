"""Starts the main interface. To be called with 'python interface'
from the root folder. After importing it, the interface will be
started start"""

import logging
import logging.handlers
import socket
import sys

from autobahn.twisted.websocket import WebSocketClientProtocol, \
                                       WebSocketClientFactory
from twisted.internet import reactor

import logger
import basic_interface as interface

# if "--localhost" in sys.argv or "-L" in sys.argv:
#     IP = "127.0.0.1"
# else:
#     IP = "192.168.178.46"


logger.initialize()
LOGGER = logging.getLogger(__name__)


def wait_for_server_ip():

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(15)

    # Bind the socket to the port
    host = ""
    port = 10000
    LOGGER.info('starting up on %s port %s', host, port)
    interface.print_msg("Waiting for a broadcast from the server.")
    sock.bind((host, port))
    # expects (host, port) as arg, two brackets are on purpose
    data = None

    try:
        LOGGER.info('waiting to receive message')
        data, address = sock.recvfrom(4096)

        LOGGER.info('received %d bytes from %s', len(data), address)
        LOGGER.info(data)
        interface.print_msg('Received %s from %s' % (data, address))

    finally:
        sock.close()

        if data and data.split(":")[0] == "sam.ip.broadcast":
            ip, port = address[0], int(data.split(":")[1])
            LOGGER.info("Used the broadcasted IP.")
            interface.print_msg("Used the broadcasted IP.")
        else:
            ip, port = None, None
            LOGGER.info("No broadcast received.")
            interface.print_msg("No broadcast received.")
        return ip, port


class Interface(WebSocketClientProtocol):

    def onConnect(self, response):
        LOGGER.info("Server connected: %s", response.peer)
        interface.on_connect(response)

    def onOpen(self):
        LOGGER.info("Connection open.")
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
                if val == "exit_server":
                    interface.on_exit()
                    self.sendClose()
                    # TODO: Close when the server closed the connection
                else:
                    self.factory.reactor.callLater(0.01, sendInput)

        self.factory.reactor.callLater(0.01, sendInput)

    def onMessage(self, payload, isBinary):
        interface.on_message(payload, isBinary)
        if isBinary:
            LOGGER.info("Binary message received: %d", len(payload))
        else:
            LOGGER.info("Text message received: %s", payload.decode('utf8'))

    def onClose(self, wasClean, code, reason):
        LOGGER.warn("The connection has been ended.")
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

    factory = WebSocketClientFactory()
    factory.protocol = Interface

    if "--localhost" in sys.argv or "-L" in sys.argv:
        ip, port = "127.0.0.1", 19113
        LOGGER.info("Used the local IP as requested per commandline-arg.")
        interface.print_msg(
            "Used the local IP as requested per commandline-arg.")
    else:
        ip, port = wait_for_server_ip()

    if ip:
        reactor.connectTCP(ip, port, factory)
        reactor.run()
    else:
        interface.on_close(False, None, "No Server found.")
