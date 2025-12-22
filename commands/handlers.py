from fastapi import HTTPException,status
from db.models import Board,Card
from commands.boards import CreateBoardCommand,UpdateBoardCommand,DeleteBoardCommand
from commands.cards import CreateCardCommand,UpdateCardCommand,DeleteCardCommand

class BoardCommandHandler:
    def __init__(self,db):
        self.db=db
    
    def handle(self,command):
        if isinstance(command,CreateBoardCommand):
            return self._create_board(command)
        if isinstance(command,UpdateBoardCommand):
            return self._update_board(command)
        if isinstance(command,DeleteBoardCommand):
            return self._delete_board(command)
        raise ValueError("Unsupported Command")

    def _create_board(self,command:CreateBoardCommand):
        board=Board(name=command.name,description=command.description,created_by=command.user_id)
        self.db.add(board)
        self.db.commit()
        self.db.refresh(board)
        return board
    
    def _update_board(self,command:UpdateBoardCommand):
        board=(self.db.query(Board).filter(Board.id==command.board_id,Board.created_by==command.user_id).first())
        if not board:
            raise HTTPException(404,"Board not found")
        
        if command.name is not None:
            board.name=command.name
        if command.description is not None:
            board.description=command.description
        
        self.db.commit()
        return board

    def _delete_board(self,command:DeleteBoardCommand):
        board=(self.db.query(Board).filter(Board.id==command.board_id,Board.created_by==command.user_id).first())
        if not board:
            raise HTTPException(404,"Board not found")
        
        self.db.delete(board)
        self.db.commit()
        return board

class CardCommandHandler:
    def __init__(self,db):
        self.db=db
    
    def handle(self,command):
        if isinstance(command,CreateCardCommand):
            return self._create_card(command)
        if isinstance(command,UpdateCardCommand):
            return self._update_card(command)
        if isinstance(command,DeleteCardCommand):
            return self._delete_card(command)

    def _create_card(self,command:CreateCardCommand):
        board=self.db.query(Board).filter(Board.id==command.board_id,Board.created_by==command.user_id)
        if board is None:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found"
        )
        card=Card(title=command.title,description=command.description,board_id=command.board_id,position=command.position,created_by=command.user_id)
        self.db.add(card)
        self.db.commit()
        self.db.refresh(card)
        return card

    def _update_card(self,command:UpdateCardCommand):
        board=self.db.query(Board).filter(Board.id==command.board_id,Board.created_by==command.user_id)
        if board is None:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found"
        )
        card=(self.db.query(Card).filter(Card.id==command.id,Card.board_id==command.board_id).first())
        if card is None:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found"
            )
        if command.title is not None:
            card.title=command.title
        if command.description is not None:
            card.description=command.description
        if command.position is not None:
            card.position=command.position
        self.db.commit()
        return card
    
    def _delete_card(self,command:DeleteCardCommand):
        board=self.db.query(Board).filter(Board.id==command.board_id,Board.created_by==command.user_id)
        if board is None:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found"
        )
        card=(self.db.query(Card).filter(Card.id==command.id,Card.board_id==command.board_id).first())
        if card is None:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found"
            )
        self.db.delete(card)
        self.db.commit()
        return card


        

    


