from pydantic import BaseModel


class BaseMessage(BaseModel):
    method: str


class InitClientMessage(BaseMessage):
    client_id: int


class ReadyMessage(BaseMessage):
    playerName: str


class QuitMessage(BaseMessage):
    pass


model_registry = {
    "init_client": InitClientMessage,
    "ready": ReadyMessage,
    "quit": QuitMessage,
}
