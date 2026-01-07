from .celery_config import celery_app
from db.database import SessionLocal
from db.models import AuditLog

@celery_app.task(name="tasks.audit.log_audit")
def log_audit(actor_id,board_id,action,payload):
    db=SessionLocal()
    try:
        db.add(AuditLog(actor_id=actor_id,board_id=board_id,action=action,payload=payload,))
        db.commit()
    finally:
        db.close()