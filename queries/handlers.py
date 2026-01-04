from queries.boards import GetBoardQuery,ListBoardsQuery,ListAccessibleBoardsQuery
from queries.cards import ListCardQuery,GetCardQuery
from fastapi import HTTPException,status
from utils.auth_utils import require_board_role
from db.models import Board,Card,BoardMembers,BoardRole

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
     
    def _get_board(self,query:GetBoardQuery):
        membership=(self.db.query(BoardMembers).filter(BoardMembers.board_id==query.id,Board.created_by==query.user_id).first())
        if not membership:
            raise HTTPException(404,"Board not found")
        board=self.db.query(Board).filter(Board.id==query.id).first()
        return board
    
    def _list_boards(self,query:ListBoardsQuery):
        boards=(self.db.query(Board).filter(Board.created_by==query.user_id).all())
        if not boards:
            raise HTTPException(404,"Boards not found")
        return boards
    
    def _list_accessible_boards(self,query:ListAccessibleBoardsQuery):
        boards = (self.db.query(Board).join(BoardMembers,Board.created_by==BoardMembers.board_id).filter(BoardMembers.user_id==query.user_id).all())
        return boards


class CardQueryHandler:
    def __init__(self,db):
        self.db=db
    
    def handle(self,query):
        if isinstance(query,GetCardQuery):
            return self._get_card(query)
        if isinstance(query,ListCardQuery):
            return self._list_cards(query)

    def _get_card(self,query:GetCardQuery):
        card=(self.db.query(Card).filter(Card.id==query.id,Card.board_id==query.board_id,Card.created_by==query.user_id).first())
        if card is None:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found"
        )
        return card
    
    def _list_cards(self,query:ListCardQuery):
        board_exists = (
        self.db.query(Board.id)
        .filter(
            Board.id == query.board_id,
            Board.created_by == query.user_id
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
            Card.board_id == query.board_id,
            Card.created_by == query.user_id
        )
        .order_by(Card.position)
        .all()
        )

    # 3. Empty list is valid
        return cards

