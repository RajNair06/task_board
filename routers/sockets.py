from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from utils.auth_utils import decode_access_token
from utils.permission_utils import BoardPermissionService
from utils.connection_manager import manager
from db.database import SessionLocal

router = APIRouter(tags=["sockets"])


@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    print("WS CONNECT ATTEMPT")

    await ws.accept()
    print("WS ACCEPTED")

    token = ws.query_params.get("token")
    if not token:
        print("WS CLOSE → missing token")
        await ws.close(code=1008)
        return

    try:
        payload = decode_access_token(token)
        print("WS AUTH OK → payload:", payload)
    except Exception as e:
        print("WS AUTH FAILED:", e)
        await ws.close(code=1008)
        return

    user_id = payload["id"]
    board_id = None

    try:
        while True:
            message = await ws.receive_json()
            print("WS MESSAGE RECEIVED:", message)

            if message["type"] == "join":
                print("JOIN REQUEST → user:", user_id)

                if board_id is not None:
                    print("JOIN REJECTED → already joined")
                    await ws.send_json({
                        "type": "error",
                        "message": "already joined a board"
                    })
                    continue

                requested_board_id = int(message["board_id"])
                print("JOIN BOARD ID:", requested_board_id)

                db = SessionLocal()
                try:
                    BoardPermissionService.require_member(
                        db=db,
                        board_id=requested_board_id,
                        user_id=user_id
                    )
                    print("BOARD PERMISSION OK")
                except Exception as e:
                    print("BOARD PERMISSION FAILED:", e)
                    await ws.send_json({
                        "type": "error",
                        "message": "unauthorized board access"
                    })
                    continue
                finally:
                    db.close()

                board_id = requested_board_id
                await manager.connect(board_id, ws)

                print(
                    "WS JOINED → board:", board_id,
                    "connections:",
                    len(manager.active_connections.get(board_id, []))
                )

                await ws.send_json({
                    "type": "joined",
                    "board_id": board_id
                })

            elif message["type"] == "leave":
                print("LEAVE REQUEST → board:", board_id)

                if board_id is not None:
                    await manager.disconnect(board_id, ws)
                    print("WS LEFT → board:", board_id)
                    board_id = None

    except WebSocketDisconnect:
        print("WS DISCONNECT")

        if board_id is not None:
            await manager.disconnect(board_id, ws)
            print("WS CLEANUP DISCONNECT → board:", board_id)
