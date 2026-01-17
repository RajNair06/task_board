from db.models import AuditLog,AuditAction,ActivityFeed,User
from db.database import SessionLocal
from .celery_config import celery_app

class ActivityMessageBuilder:
    @staticmethod
    def build(audit:AuditLog,name:str):
        if audit.action==AuditAction.BOARD_CREATED:
            return f"{name} created the board {audit.payload["name"]},description: {audit.payload["description"]}"
        elif audit.action==AuditAction.BOARD_UPDATED:
            return f"{name} updated the board title:'{audit.payload["old"]["name"]}',description '{audit.payload["old"]["description"]}' to '{audit.payload["new"]["name"]}',description {audit.payload["new"]["description"]}"
        elif audit.action==AuditAction.BOARD_DELETED:
            return f"{name} deleted the board with id {audit.board_id}"
        elif audit.action==AuditAction.CARD_CREATED:
            return f"{name} created the card with title:{audit.payload["title"]},description:{audit.payload["description"]}"
        elif audit.action==AuditAction.CARD_DELETED:
            return f"removed a card from board id {audit.board_id}"
        elif audit.action==AuditAction.CARD_UPDATED:
            return f"{name} updated the card with title:{audit.payload["old"]["title"]},desc:{audit.payload["old"]["description"]},position:{audit.payload["old"]["position"]} to title:{audit.payload["new"]["title"]},desc:{audit.payload["new"]["description"]},position:{audit.payload["new"]["position"]}" 
        elif audit.action==AuditAction.MEMBER_ADDED:
            return f"{name} added a member to the board-{audit.payload["board_id"]} with user id {audit.payload["target_user_id"]} and role {audit.payload["role"]}"
        elif audit.action==AuditAction.MEMBER_REMOVED:
            return f"{name} removed a member from the board-{audit.payload["board_id"]} with user id  {audit.payload["user_id"]}"
        elif audit.action==AuditAction.MEMBER_ROLE_CHANGED:
            return f"{name} updated member role from board-{audit.payload["board_id"]} with user id {audit.payload["user_id"]} from role {audit.payload["old_role"]} to {audit.payload["new_role"]} "
        
        return f"{name} performed an action"

@celery_app.task(name="tasks.feed.log")
def build_activity_from_audit(audit_log_id:int):
    db=SessionLocal()
    try:

        audit=db.get(AuditLog,audit_log_id)
        actor=db.get(User,audit.actor_id)
        actor_name=actor.name


        message=ActivityMessageBuilder.build(audit,actor_name)
        activity=ActivityFeed(board_id=audit.board_id,actor_id=audit.actor_id,activity_type=audit.action,message=message,metadata_info=audit.payload)
        db.add(activity)
        db.commit()
    finally:
        db.close()