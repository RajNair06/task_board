from collections import defaultdict
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, set[WebSocket]] = defaultdict(set)
        
    async def connect(self, board_id: int, ws: WebSocket):
        self.active_connections[board_id].add(ws)
        

    async def disconnect(self, board_id: int, ws: WebSocket):
        self.active_connections[board_id].discard(ws)
        

        if not self.active_connections[board_id]:
            print(f"BOARD {board_id} HAS NO ACTIVE CONNECTIONS")

    async def broadcast(self, board_id: int, message: dict):
        connections = self.active_connections.get(board_id, set())

        print(
            f"BROADCAST ATTEMPT → board={board_id} "
            f"connections={len(connections)} "
            f"payload_type={message.get('type')}"
        )

        if not connections:
            print(f"BROADCAST ABORTED → no connections for board {board_id}")
            return

        dead_sockets = []

        for ws in connections:
            try:
                await ws.send_json(message)
                print("WS MESSAGE SENT")
            except Exception as e:
                print("WS SEND FAILED:", repr(e))
                dead_sockets.append(ws)

        # cleanup broken sockets
        for ws in dead_sockets:
            self.active_connections[board_id].discard(ws)
            print("REMOVED DEAD SOCKET")

        print(
            f"BROADCAST COMPLETE → board={board_id} "
            f"remaining_connections={len(self.active_connections[board_id])}"
        )


manager = ConnectionManager()