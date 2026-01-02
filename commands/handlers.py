from fastapi import HTTPException,status
from db.models import Board,Card,BoardMembers,BoardRole
from utils.permission_utils import BoardPermissionService
from commands.boards import CreateBoardCommand,UpdateBoardCommand,DeleteBoardCommand
from commands.cards import CreateCardCommand,UpdateCardCommand,DeleteCardCommand
from commands.boards import AddBoardMemberCommand,UpdateBoardMemberRoleCommand,RemoveBoardMemberCommand

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
        self.db.flush()
        membership=BoardMembers(user_id=command.user_id,board_id=board.id,role=BoardRole.owner,)
        self.db.add(membership)
        self.db.commit()
        self.db.refresh(board)
        return board
    
    def _update_board(self,command:UpdateBoardCommand):
        BoardPermissionService.require_role(db=self.db,board_id=command.board_id,user_id=command.user_id,allowed_roles={BoardRole.owner,BoardRole.editor})
        board=(self.db.query(Board).filter(Board.id==command.board_id).first())
        if not board:
            raise HTTPException(404,"Board not found")
        
        if command.name is not None:
            board.name=command.name
        if command.description is not None:
            board.description=command.description
        
        self.db.commit()
        return board

    def _delete_board(self,command:DeleteBoardCommand):
        BoardPermissionService.require_role(db=self.db,board_id=command.board_id,user_id=command.user_id,allowed_roles={BoardRole.owner})
        board=(self.db.query(Board).filter(Board.id==command.board_id).first())
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


        
class BoardMemberHandler:
    def __init__(self,db):
        self.db=db
    
    def handle(self,command):
        if isinstance(command,AddBoardMemberCommand):
            return self._add_member(command)
    
    def _require_owner(self,board_id,user_id):
        BoardPermissionService.require_role(db=self.db,board_id=board_id,user_id=user_id,allowed_roles={BoardRole.owner})
    
    def _add_member(self,command:AddBoardMemberCommand):
        self._require_owner(command.board_id,command.owner_id)

        if command.role==BoardRole.owner:
            raise HTTPException(400,"owner role cannot be assigned")
        
        exists=(self.db.query(BoardMembers).filter(BoardMembers.board_id==command.board_id,BoardMembers.user_id==command.target_user_id).first())
        if exists:
            raise HTTPException(400,"owner role cannot be assigned")
        
        membership=BoardMembers(board_id=command.board_id,user_id=command.target_user_id,role=command.role)
        self.db.add(membership)
        self.db.commit()
        return membership

    def _remove_member(self,command:RemoveBoardMemberCommand):
        self._require_owner(command.board_id,command.owner_id)
        membership=(self.db.query(BoardMembers).filter(BoardMembers.board_id==command.board_id).first())
        if not membership:
            raise HTTPException(400,"member not found")

        if membership.role==BoardRole.owner:
            raise HTTPException(400,"owner cant be removed")
        self.db.delete(membership)
        self.db.commit()
    
    def _update_role(self,command:UpdateBoardMemberRoleCommand):
        self._require_owner(command.board_id,command.owner_id)
        if command.new_role==BoardRole.owner:
            raise HTTPException(400,"owner role cannot be assigned")
        membership=(self.db.query(BoardMembers).filter(BoardMembers.board_id==command.board_id,BoardMembers.user_id==command.target_user_id).first())

        if not membership:
            raise HTTPException(400,"member not found")
        
        membership.role=command.new_role
        self.db.commit()
        return membership


    
    

    


