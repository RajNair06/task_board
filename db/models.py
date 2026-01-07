from sqlalchemy.orm import declarative_base,relationship
from sqlalchemy import Column,Integer,DateTime,func,String,ForeignKey,Enum,Index,Text,Numeric,Boolean,JSON
import enum

from datetime import datetime
Base=declarative_base()


class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False)
    email=Column(String,unique=True,nullable=False)
    password_hash=Column(String,nullable=False)
    created_at=Column(DateTime,default=datetime.now())
    updated_at=Column(DateTime,onupdate=datetime.now())
    boards=relationship("BoardMembers",back_populates="user")


    def __repr__(self):
        return f"{self.name}->{self.email}"
    
class Board(Base):
    __tablename__="boards"
    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False)
    description=Column(Text,nullable=True)
    created_at=Column(DateTime,default=datetime.now())
    created_by=Column(Integer,ForeignKey("users.id"),nullable=False)
    updated_at=Column(DateTime,onupdate=datetime.now(),default=datetime.now())
    members=relationship("BoardMembers",back_populates="board",cascade="all,delete-orphan",passive_deletes=True)


class BoardRole(enum.Enum):
    owner = "owner"
    editor = "editor"
    viewer = "viewer"


class BoardMembers(Base):
    __tablename__="board_members"
    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id"))
    board_id=Column(Integer,ForeignKey("boards.id"))
    role = Column(
        Enum(BoardRole, name="board_role_enum", create_constraint=True),
        nullable=False
    )
    user=relationship("User",back_populates="boards")
    board=relationship("Board",back_populates="members")


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    is_complete=Column(Boolean,default=False)
    
    board_id = Column(Integer, ForeignKey("boards.id"), nullable=False, index=True)
    position = Column(Numeric(10, 2), nullable=False)
    
    
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.now(),
        onupdate=datetime.now(),
        nullable=False,
    )

class AuditAction:
    BOARD_CREATED="BOARD_CREATED"
    BOARD_UPDATED="BOARD_UPDATED"
    BOARD_DELETED="BOARD_DELETED"
    CARD_CREATED="CARD_CREATED"
    CARD_UPDATED="CARD_UPDATED"
    CARD_DELETED="CARD_DELETED"
    MEMBER_ADDED="MEMBER_ADDED"
    MEMBER_REMOVED="MEMBER_REMOVED"
    MEMBER_ROLE_CHANGED="MEMBER_ROLE_CHANGED"

class AuditLog(Base):
    __tablename__="audit_logs"
    id=Column(Integer,primary_key=True)
    actor_id=Column(Integer,nullable=False)
    board_id=Column(Integer,nullable=False,index=True)
    action=Column(String,nullable=False)
    payload=Column(JSON,nullable=True)
    created_at=Column(DateTime,default=datetime.now,nullable=False)
    



Index("ix_cards_board_position", Card.board_id, Card.position)
Index("ix_boards_owner_id", Board.created_by)

