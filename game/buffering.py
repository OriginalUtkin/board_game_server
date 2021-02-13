import json
import struct


def send_stream(obj):
    s = json.dumps(obj).encode("utf-16-le")
    l = struct.pack("<i", len(s))
    s = l + s
    return s


class ReceiveBuffer:
    def __init__(self):
        self.buff = ""

    def receive(self, s):
        self.buff += s

    def get_message(self):
        if len(self.buff) < 4:
            return None
        l = struct.unpack("<i", self.buff[:4])[0]
        if len(self.buff) < (4 + l):
            return None
        msg = self.buff[4 : 4 + l]
        self.buff = self.buff[4 + l :]
        return json.loads(msg.decode("utf-16"))
