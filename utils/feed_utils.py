import asyncio
from db.database import SessionLocal
from db.models import ActivityFeed

last_sent_activity_id: dict[int, int] = {}

async def activity_feed_dispatcher(manager):
    

    while True:
        
        await asyncio.sleep(1)

        db = SessionLocal()
        try:
            
            for board_id, connections in manager.active_connections.items():
                if not connections:
                        continue

                last_id = last_sent_activity_id.get(board_id, 0)
                feeds = (
                    db.query(ActivityFeed)
                    .filter(
                        ActivityFeed.board_id == board_id,
                        ActivityFeed.id > last_id
                    )
                    .order_by(ActivityFeed.id.asc())
                    .all()
                 )
                for feed in feeds:
                    payload = {
                        "type": "activity",
                        "board_id": feed.board_id,
                        "actor_id": feed.actor_id,
                        "activity_type": feed.activity_type,
                        "message": feed.message,
                        "created_at": feed.created_at.isoformat(),
                    }

                    await manager.broadcast(feed.board_id, payload)

                    last_sent_activity_id[board_id] = feed.id
                    

        except Exception as e:
            print("error:", e)

        finally:
            db.close()
