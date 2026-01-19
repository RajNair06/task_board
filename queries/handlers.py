from queries.boards import GetBoardQuery,ListBoardsQuery,ListAccessibleBoardsQuery,ActivityFeedQuery
from queries.cards import ListCardQuery,GetCardQuery
from queries.feed import ActivityFeedQuery
from fastapi import HTTPException,status
from utils.permission_utils import BoardPermissionService
from db.models import Board,Card,BoardMembers,BoardRole,ActivityFeed
from sqlalchemy import select

class ActivityQueryHandler:
    def __init__(self,db):
        self.db=db
    
    def handle(self,query):
        if isinstance(query,ActivityFeedQuery):
            return self._list_activity_feed(query)
        
    def _list_activity_feed(self,query:ActivityFeedQuery):
            BoardPermissionService.require_member(db=self.db,board_id=query.board_id,user_id=query.user_id)
            stmt = (
            select(
            ActivityFeed.actor_id,
            ActivityFeed.message,
            ActivityFeed.activity_type,
            ActivityFeed.created_at,
            ActivityFeed.metadata_info,
            ).where(ActivityFeed.board_id == query.board_id).order_by(ActivityFeed.created_at.desc()))
            result = self.db.execute(stmt).mappings().all()
            return result


class BoardQueryHandler:
    def __init__(self,db):
        self.db=db
    
    def handle(self,query):
        if isinstance(query,GetBoardQuery):
            return self._get_board(query)
        if isinstance(query,ListBoardsQuery):
            return self._list_boards(query)
        if isinstance(query,ListAccessibleBoardsQuery):
            return self._list_accessible_boards(query)
        if isinstance(query,ActivityFeedQuery):
            return self._list_activity_feed(query)
     
    def _get_board(self,query:GetBoardQuery):
        membership=(self.db.query(BoardMembers).filter(BoardMembers.board_id==query.id,BoardMembers.user_id==query.user_id).first())
        if not membership:
            raise HTTPException(status_code=401,detail="Not authorized")
        board=self.db.query(Board).filter(Board.id==query.id).first()
        return {
            "id": board.id,
            "name": board.name,
            "description": board.description,
            "created_by": board.created_by,
            "created_at": board.created_at,
            "updated_at": board.updated_at,
        }
    
    def _list_boards(self,query:ListBoardsQuery):
        boards=(self.db.query(Board).filter(Board.created_by==query.user_id).all())
        if not boards:
            raise HTTPException(404,"Boards not found")
        return [
            {
                "id": board.id,
                "name": board.name,
                "description": board.description,
                "created_by": board.created_by,
                "created_at": board.created_at,
                "updated_at": board.updated_at,
            }
            for board in boards
        ]
    
    def _list_accessible_boards(self,query:ListAccessibleBoardsQuery):
        boards = (self.db.query(Board).join(BoardMembers,Board.created_by==BoardMembers.board_id).filter(BoardMembers.user_id==query.user_id).all())
        if not boards:
            raise HTTPException(404,"Boards not found")
        return [
            {
                "id": board.id,
                "name": board.name,
                "description": board.description,
                "created_by": board.created_by,
                "created_at": board.created_at,
                "updated_at": board.updated_at,
            }
            for board in boards
        ]
    
    def _list_activity_feed(self,query:ActivityFeedQuery):
        BoardPermissionService.require_member(db=self.db,board_id=query.board_id,user_id=query.user_id)
        activities=(
            self.db.query(ActivityFeed).filter(ActivityFeed.board_id==query.board_id).order_by(ActivityFeed.created_at.desc()).limit(50))
        return [
            {
                "actor_id": activity.actor_id,
                "message": activity.message,
                "activity_type": activity.activity_type,
                "created_at": activity.created_at,
                "metadata_info": activity.metadata_info,
            }
            for activity in activities
        ]

        
        


class CardQueryHandler:
    def __init__(self,db):
        self.db=db
    
    def handle(self,query):
        if isinstance(query,GetCardQuery):
            return self._get_card(query)
        if isinstance(query,ListCardQuery):
            return self._list_cards(query)

    def _get_card(self,query:GetCardQuery):
        BoardPermissionService.require_member(self.db,query.board_id,query.user_id)
        card=(self.db.query(Card).filter(Card.id==query.id,Card.board_id==query.board_id).first())
        if card is None:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found"
        )
        return {
            "id": card.id,
            "title": card.title,
            "description": card.description,
            "is_complete": card.is_complete,
            "board_id": card.board_id,
            "position": card.position,
            "created_by": card.created_by,
            "created_at": card.created_at,
            "updated_at": card.updated_at,
        }
    
    def _list_cards(self,query:ListCardQuery):
        BoardPermissionService.require_member(self.db,query.board_id,query.user_id)
        board_exists = (
        self.db.query(Board.id)
        .filter(
            Board.id == query.board_id,
            
        )
        .first()
        )

        if not board_exists:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found"
            )

    # 2. Fetch cards
        cards = (
        self.db.query(Card)
        .filter(
            Card.board_id == query.board_id
            
        )
        .order_by(Card.position)
        .all()
        )

    # 3. Empty list is valid
        return [
            {
                "id": card.id,
                "title": card.title,
                "description": card.description,
                "is_complete": card.is_complete,
                "board_id": card.board_id,
                "position": card.position,
                "created_by": card.created_by,
                "created_at": card.created_at,
                "updated_at": card.updated_at,
            }
            for card in cards
        ]

