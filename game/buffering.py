import json
import struct
from typing import Dict


def send_stream(obj) -> bytes:
    raw_json = json.dumps(obj).encode("utf-16-le")
    string_length = struct.pack("<i", len(raw_json))
    raw_json = string_length + raw_json
    return raw_json


class ReceiveBuffer:
    def __init__(self):
        self.buff = b""

    def receive(self, s):
        self.buff += s

    def get_message(self) -> Dict:
        if len(self.buff) < 4:
            return None
        l = struct.unpack("<i", self.buff[:4])[0]
        if len(self.buff) < (4 + l):
            return None
        msg = self.buff[4 : 4 + l]
        self.buff = self.buff[4 + l :]

        print("get_message", msg.decode("utf-16"))
        return json.loads(msg.decode("utf-16"))
