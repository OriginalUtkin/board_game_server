from typing import Dict


class GameServer:
    last_id = 0
    last_print = 0
    prints_per_sec = 2
    clients: Dict = {}  # list of connected clients
