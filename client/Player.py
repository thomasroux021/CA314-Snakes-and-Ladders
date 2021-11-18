import Piece 

class Player:
    def __init__(self, userId, userName) -> None:
        self.uid = userId
        self.name = userName
        self.piece = None
        self.turn = False

    def set_piece(self, piece):
        self.piece = piece
    
    def get_piece(self) -> Piece:
        return self.piece