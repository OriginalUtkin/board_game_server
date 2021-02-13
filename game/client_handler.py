from twisted.internet import protocol, reactor
from twisted.internet.protocol import connectionDone

from .buffering import ReceiveBuffer, send_stream
from .server import GameServer


class GameClient(protocol.Protocol):
    def __init__(self):
        # client connected
        self.client_id = GameServer.last_id
        GameServer.last_id += 1
        GameServer.clients[self.client_id] = self

        self.buff = ReceiveBuffer()

    def dataReceived(self, data):
        # collect data, parse message when its ready
        self.buff.receive(data)
        while 1:
            message = self.buff.get_message()
            if message is None:
                break
            self._handle_message(message)

    def connectionLost(self, reason=connectionDone):  # pylint: disable=unused-argument
        GameServer.clients.pop(self.client_id)

    def _handle_message(self, message):
        # pick message handler
        if message["method"] == "ready":
            self._handle_ready(message)

    def _handle_ready(self, _):
        # simple reply to client
        s = send_stream({"method": "init_client", "new_id": 123})
        self.transport.write(s)


def serverIdle():
    reactor.callLater(2.00, serverIdle)

    # idle game logic here
    # for example, turn time limit can be controlled here


class GameClientFactory(protocol.Factory):
    def buildProtocol(self, addr):  # pylint: disable=unused-argument
        return GameClient()
