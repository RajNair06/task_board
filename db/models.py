from sqlalchemy.orm import declarative_base,relationship
from sqlalchemy import Column,Integer,DateTime,func,String,ForeignKey,Enum,Index,Text,Numeric,Boolean
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
    user_id=Column(Integer,ForeignKey("users.id"),primary_key=True)
    board_id=Column(Integer,ForeignKey("boards.id"),primary_key=True)
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





Index("ix_cards_board_position", Card.board_id, Card.position)
Index("ix_boards_owner_id", Board.created_by)

