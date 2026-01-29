import os
import asyncio
from db.database import SessionLocal
from db.models import ActivityFeed
import redis.asyncio as redis
import json

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

REDIS_URL = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")

async def redis_listener(manager):
     client=redis.from_url(REDIS_URL)
     pubsub=client.pubsub()
     await pubsub.psubscribe("board:*")
     print("subscribed to board channel")
     try:
        async for message in pubsub.listen():
            
            if message is None:
                    continue
            msg_type=message.get("type")
            if msg_type not in ("message","pmessage"):
                    continue
            raw_channel=message.get("channel")
            channel=raw_channel.decode() if isinstance(raw_channel,bytes) else raw_channel
            raw_data=message.get("data")
            data=raw_data.decode() if isinstance(raw_data,bytes) else raw_data
              
            event=json.loads(data)
            board_id=int(channel.split(":")[1])
            await manager.broadcast(board_id,event)
            
     
     except Exception as e:
        print(e)
     finally:
        await pubsub.unsubscribe()
        await pubsub.close()
        await client.close()
                

          
