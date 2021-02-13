from typing import Dict, cast

from pydantic import BaseModel
from twisted.internet import protocol, reactor
from twisted.internet.protocol import connectionDone

from .buffering import ReceiveBuffer, send_stream
from .models import InitClientMessage, QuitMessage, ReadyMessage, model_registry
from .server import GameServer


class GameClient(protocol.Protocol):
    def __init__(self):
        # client connected
        print("player connected")

        self.client_id = GameServer.last_id
        GameServer.last_id += 1
        GameServer.clients[self.client_id] = self
        self.buff = ReceiveBuffer()

        self._handlers = {
            "ready": self._handle_ready,
            "quit": self._handle_quit,
        }

    def dataReceived(self, data):
        # collect data, parse message when its ready
        self.buff.receive(data)
        while 1:
            message = self.buff.get_message()
            if message is None:
                break
            self._handle_message(message)

    def connectionLost(self, reason=connectionDone):  # pylint: disable=unused-argument
        print("connectionLost")
        GameServer.clients.pop(self.client_id)

    def _send_message(self, message: BaseModel):
        raw_msg = send_stream(message.dict())
        self.transport.write(raw_msg)

    def _handle_message(self, message: Dict):
        # pick message handler
        print("_handle_message", message)

        handler = self._handlers[message["method"]]
        model = cast(BaseModel, model_registry[message["method"]])
        handler(model.parse_obj(message))

    def _handle_ready(self, message: ReadyMessage):
        # simple reply to client
        print("_handle_ready", message)
        self._send_message(
            InitClientMessage(method="init_client", client_id=self.client_id)
        )
        print("init_client sent")

    def _handle_quit(self, message: QuitMessage):
        # simple reply to client
        print("_handle_quit", message)


def serverIdle():
    reactor.callLater(2.00, serverIdle)

    # idle game logic here
    # for example, turn time limit can be controlled here


class GameClientFactory(protocol.Factory):
    def buildProtocol(self, addr):  # pylint: disable=unused-argument
        return GameClient()
