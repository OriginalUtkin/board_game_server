import signal
import sys

from twisted.internet import reactor
from twisted.python import log

from game.client_handler import GameClientFactory, serverIdle


def handler_SIGINT(_, __):
    reactor.stop()


def start_server():
    log.startLogging(sys.stderr)
    signal.signal(signal.SIGINT, handler_SIGINT)

    reactor.listenTCP(20140, GameClientFactory())
    reactor.callLater(2.00, serverIdle)

    reactor.run(installSignalHandlers=0)


if __name__ == "__main__":
    start_server()
